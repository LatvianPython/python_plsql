from __future__ import annotations

from collections import namedtuple
from functools import wraps
from itertools import groupby
from operator import attrgetter
from operator import itemgetter
from typing import Iterator
from typing import List
from typing import Optional
from typing import TYPE_CHECKING

from .conversion import cursor_var
from .conversion import to_python
from .introspection import Argument
from .introspection import Direction
from .introspection import ObjectTypes
from .introspection import ResolvedName

if TYPE_CHECKING:
    from .database import Database


def return_type(arguments: List[Argument]) -> Optional[Argument]:
    """
    Extracts return type from list of arguments.
    According to Oracle documentation: "Position 0 returns the values for the return type of a function."
    """
    for argument in arguments:
        if argument.position == 0:
            return argument


class Overload:
    def __init__(self, arguments: Iterator[Argument]):
        self.arguments = list(arguments)

        self.return_type: Argument = return_type(self.arguments)

        self.arguments = [
            argument
            for argument in self.arguments
            if argument.position and argument.datatype and argument.level == 0
        ]

    def match(self, *args, **kwargs) -> bool:
        argument_count = len(args) + len(kwargs)

        exact_match = argument_count == len(self.arguments)

        if argument_count < len(self.arguments):
            return argument_count == len(
                [argument for argument in self.arguments if not argument.default_value]
            )
        return exact_match

    def argument(self, name: str) -> Optional[Argument]:
        for argument in self.arguments:
            if argument.argument_name == name.upper():
                return argument

    @property
    def is_function(self) -> bool:
        return bool(self.return_type)


def group_by_overload(arguments: Iterator[Argument]) -> List[Overload]:
    return [
        Overload(arguments=grouped_arguments)
        for _, grouped_arguments in groupby(arguments, attrgetter("overload"))
    ] or [Overload(arguments=[])]


def find_match(
    overloads: List[Overload], filter_function, *positional, **named
) -> Overload:

    matches = [
        overload
        for overload in overloads
        if overload.match(*positional, **named)
        if filter_function(overload)
    ]

    if len(matches) > 1:
        raise ValueError("Arguments matched with too many subprograms")
    elif len(matches) == 0:
        raise ValueError("Arguments do not match subprogram")
    return matches[0]


def wrap_positional(match, plsql, resolved, cursor, positional):
    wrapped_positional = []
    for value, argument in zip(positional, match.arguments):
        _, converter = cursor_var(plsql, cursor, resolved, argument)

        wrapped_positional.append(converter.to_oracle(value))

    return wrapped_positional


def wrap_named(match, plsql, resolved, cursor, named):
    wrapped_named = {}
    for key, value in named.items():
        argument = match.argument(key)
        if argument:
            _, converter = cursor_var(plsql, cursor, resolved, argument)
            wrapped_named[key] = converter.to_oracle(value)

    return wrapped_named


def in_out_parameters(positional, named, match: Overload):
    in_out = []
    for pos, argument in zip(positional, match.arguments):
        if argument.in_out in {Direction.out, Direction.in_out}:
            in_out.append((pos, argument.argument_name.lower()))

    for argument in match.arguments:
        if argument.in_out in {Direction.out, Direction.in_out}:
            try:
                in_out.append(
                    (
                        named[argument.argument_name.lower()],
                        argument.argument_name.lower(),
                    )
                )
            except KeyError:
                pass

    in_out_rec = namedtuple("InOutParams", map(itemgetter(1), in_out))

    return in_out_rec(*map(to_python, map(itemgetter(0), in_out)))


def translate_arguments(match_filter):
    def decorator(func):
        @wraps(func)
        def wrapper(self: Subprogram, *positional, **named):
            match = find_match(self.overloads, match_filter, *positional, **named)

            with self._plsql._connection.cursor() as cursor:

                wrapped_positional = wrap_positional(
                    match, self._plsql, self.resolved, cursor, positional
                )

                wrapped_named = wrap_named(
                    match, self._plsql, self.resolved, cursor, named
                )

                result = func(self, match, cursor, wrapped_positional, wrapped_named)

                in_out = in_out_parameters(wrapped_positional, wrapped_named, match)

            if match.is_function:
                if in_out:
                    return result, in_out
                return result

            if in_out:
                return in_out

        return wrapper

    return decorator


class Subprogram:
    def __init__(
        self, plsql: Database, resolved: ResolvedName, arguments: Iterator[Argument]
    ):
        self._plsql, self.resolved, self.overloads = (
            plsql,
            resolved,
            group_by_overload(arguments=arguments),
        )

    @translate_arguments(match_filter=lambda x: x.is_function)
    def _call_function(self, match: Overload, cursor, positional, named):
        object_type, converter = cursor_var(
            plsql=self._plsql,
            cursor=cursor,
            resolved=self.resolved,
            plsql_type=match.return_type,
        )

        result = cursor.callfunc(self.resolved.name, object_type, positional, named)
        return converter.from_oracle(result)

    @translate_arguments(match_filter=lambda x: not x.is_function)
    def _call_procedure(self, match: Overload, cursor, positional, named):
        _ = match
        cursor.callproc(self.resolved.name, positional, named)

    def __call__(self, *args, **kwargs):
        if self.is_overloaded and self.is_function and self.is_procedure:
            raise NotImplementedError(
                "Subprogram is overloaded as a function and procedure, use _call_procedure or _call_function methods"
            )

        if self.is_function:
            return self._call_function(*args, **kwargs)
        else:
            return self._call_procedure(*args, **kwargs)

    @property
    def is_overloaded(self) -> bool:
        return len(self.overloads) > 1

    @property
    def is_function(self) -> bool:
        return any(overload.is_function for overload in self.overloads)

    @property
    def is_procedure(self) -> bool:
        return any(not overload.is_function for overload in self.overloads)

    @property
    def standalone(self) -> bool:
        return self.resolved.object_type in {
            ObjectTypes.procedure,
            ObjectTypes.function,
        }
