from __future__ import annotations

from collections import namedtuple
from enum import IntEnum
from functools import wraps
from itertools import groupby
from itertools import starmap
from operator import attrgetter
from operator import itemgetter
from typing import Any
from typing import Iterator
from typing import List
from typing import Optional
from typing import Tuple
from typing import Union

import cx_Oracle as oracle

Argument = namedtuple(
    "Argument",
    "overload position level argument_name datatype default_value in_out length precision scale radix",
)

ResolvedName = namedtuple(
    "ResolvedName", "schema name database_link object_type object_id subprogram_id"
)


class ObjectTypes(IntEnum):
    table = 2
    synonym = 5
    sequence = 6
    procedure = 7
    function = 8
    package = 9
    type = 13


class Direction(IntEnum):
    in_ = 0
    out = 1
    in_out = 2


class NotFound(AttributeError):
    pass


def _dbms_describe_describe_procedure(
    connection: oracle.Connection, name: str
) -> Iterator[Tuple[Any, ...]]:
    """Wrapper for Oracle DBMS_DESCRIBE.DESCRIBE_PROCEDURE procedure"""

    number_table, varchar2_table = (
        connection.gettype("SYS.DBMS_DESCRIBE.NUMBER_TABLE"),
        connection.gettype("SYS.DBMS_DESCRIBE.VARCHAR2_TABLE"),
    )

    with connection.cursor() as cursor:
        overload = number_table.newobject()
        position = number_table.newobject()
        level = number_table.newobject()
        argument_name = varchar2_table.newobject()
        datatype = number_table.newobject()
        default_value = number_table.newobject()
        in_out = number_table.newobject()
        length = number_table.newobject()
        precision = number_table.newobject()
        scale = number_table.newobject()
        radix = number_table.newobject()
        spare = number_table.newobject()

        try:
            cursor.callproc(
                "dbms_describe.describe_procedure",
                [
                    name,
                    None,
                    None,
                    overload,
                    position,
                    level,
                    argument_name,
                    datatype,
                    default_value,
                    in_out,
                    length,
                    precision,
                    scale,
                    radix,
                    spare,
                ],
            )
        except oracle.DatabaseError as err:
            if err.args[0].code == 20001:
                raise NotFound
            raise

        return zip(
            overload.aslist(),
            position.aslist(),
            level.aslist(),
            argument_name.aslist(),
            datatype.aslist(),
            map(bool, default_value.aslist()),
            map(Direction, in_out.aslist()),
            length.aslist(),
            precision.aslist(),
            scale.aslist(),
            radix.aslist(),
        )


def _dbms_utility_name_resolve(
    connection: oracle.Connection, name: str, context: int
) -> Tuple[str, str, str, str, int, int]:
    """Wrapper for Oracle DBMS_UTILITY.NAME_RESOLVE procedure"""
    with connection.cursor() as cursor:
        schema = cursor.var(str)
        part1 = cursor.var(str)
        part2 = cursor.var(str)
        database_link = cursor.var(str)
        part1_type = cursor.var(int)
        object_id = cursor.var(int)

        cursor.callproc(
            "dbms_utility.name_resolve",
            [
                name,
                context,
                schema,
                part1,
                part2,
                database_link,
                part1_type,
                object_id,
            ],
        )

        return (
            schema.getvalue(),
            part1.getvalue(),
            part2.getvalue(),
            database_link.getvalue(),
            part1_type.getvalue(),
            object_id.getvalue(),
        )


def _exhaustive_name_resolution(
    connection: oracle.Connection, name: str
) -> Tuple[str, str, str, str, int, int]:
    """Exhaustively searches for name in database using all available contexts possible in DBMS_UTILITY.NAME_RESOLVE"""
    for context in range(0, 10):
        try:
            return _dbms_utility_name_resolve(
                connection=connection, name=name, context=context
            )
        except oracle.DatabaseError as err:
            # ORA-04047: object specified is incompatible with the flag specified
            # ORA-06564: object name does not exist
            if err.args[0].code in (4047, 6564):
                continue
            raise
        else:
            break

    raise NotFound(f"name {name} not found")


class Schema:
    def __init__(self, plsql: Database, name: str):
        self._plsql, self._name = plsql, name

    def __getattr__(self, item: str) -> Optional[Union[Subprogram, Package]]:
        item = f"{self._name}.{item}"
        name = self._plsql._name_resolve(item)
        return search_object(plsql=self._plsql, name=name, item=item)


class Package:
    def __init__(self, plsql: Database, name: str):
        self._plsql, self._name = plsql, name

    def __getattr__(self, item: str) -> Subprogram:
        item = f"{self._name}.{item}"
        name = self._plsql._name_resolve(item)
        return Subprogram(
            plsql=self._plsql,
            resolved=name,
            arguments=self._plsql._describe_procedure(item),
        )


class Query:
    def __init__(
        self, connection: oracle.Connection, sql: str, *positional_binds, **named_binds
    ):
        if all([positional_binds, named_binds]):
            raise ValueError("Can not bind both by position and name")

        binds = positional_binds or named_binds

        self._connection, self.sql, self.binds = (connection, sql, binds)

    def _execute(self):
        with self._connection.cursor() as cursor:
            cursor.execute(self.sql, self.binds)

            if len(cursor.description) > 1:
                record_type = namedtuple(
                    "Record", (column[0].lower() for column in cursor.description)
                )
                records = starmap(record_type, cursor)
            else:
                records = map(itemgetter(0), cursor)

            for record in records:
                yield record

    @property
    def first(self):
        try:
            return next(self._execute())
        except StopIteration:
            return None

    def __iter__(self):
        return self._execute()


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


def plsql_record(attributes) -> Any:
    return namedtuple("Record", (attribute.name.lower() for attribute in attributes))


# noinspection PyTypeChecker
def to_python(value):
    if isinstance(value, oracle.Object):
        if value.type.attributes:
            return record_out_converter(value)
        elif is_list(value.type):
            return list_out_converter(value)
        return dict_out_converter(value)
    try:
        return value.getvalue(0)
    except AttributeError:
        return value


def to_record(value, record):
    return record._make(
        to_python(getattr(value, attribute.upper())) for attribute in record._fields
    )


def list_out_converter(value):
    if not isinstance(value.type.element_type, oracle.DbType):
        attributes = value.type.element_type.attributes
        if attributes:
            record = plsql_record(attributes)
            return [to_record(val, record) for val in value.aslist()]
        return [to_python(val) for val in value.aslist()]
    return value.aslist()


def dict_out_converter(value):
    if not isinstance(value.type.element_type, oracle.DbType):
        attributes = value.type.element_type.attributes
        if attributes:
            record = plsql_record(attributes)
            return {key: to_record(val, record) for key, val in value.asdict().items()}
        return {key: to_python(val) for key, val in value.asdict().items()}
    return value.asdict()


def record_out_converter(value, record=None):
    attributes = value.type.attributes
    record = record or plsql_record(attributes)
    return to_record(value, record)


def type_name(plsql: Database, resolved: ResolvedName, plsql_type: Argument):
    argument_type_name = plsql.query(
        """
    SELECT type_owner, type_name, type_subname
      FROM all_arguments
     WHERE object_id = :object_id
       AND position = :position
       AND subprogram_id = :subprogram_id
       AND data_level = 0
    """,
        object_id=resolved.object_id,
        position=plsql_type.position,
        subprogram_id=resolved.subprogram_id,
    ).first

    return ".".join(argument_type_name)


def convert(object_type, value):
    if isinstance(object_type, oracle.DbType):
        pass
    elif object_type:
        return make_in_converter(object_type)(value)
    return value


def make_in_converter(object_type):
    def _in_converter(value):
        var = object_type.newobject()
        if value:
            if object_type.iscollection:
                if is_list(object_type):
                    for val in value:
                        var.append(convert(object_type.element_type, val))
                else:
                    for key, val in value.items():
                        var.setelement(key, convert(object_type.element_type, val))
            else:
                for attribute, val in zip(object_type.attributes, value):
                    setattr(var, attribute.name, convert(attribute.type, val))

        return var

    return _in_converter


def is_list(object_type: oracle.ObjectType) -> bool:
    # todo: find better way
    obj = object_type.newobject()
    try:
        obj.trim(1)
    except oracle.DatabaseError:
        return True
    else:
        return False


class SimpleVar:
    def __init__(self, cursor, object_type):
        self.cursor, self.object_type = cursor, object_type

    def to_oracle(self, value):
        var = self.cursor.var(self.object_type)
        var.setvalue(0, value)
        return var

    @staticmethod
    def from_oracle(var):
        return var


class UserVar:
    def __init__(self, in_converter):
        self.in_converter = in_converter

    def to_oracle(self, value):
        return self.in_converter(value)

    @staticmethod
    def from_oracle(value):
        return to_python(value)


def cursor_var(
    plsql: Database, cursor: oracle.Cursor, resolved: ResolvedName, plsql_type: Argument
):
    plsql_types = {
        1: oracle.STRING,
        2: oracle.NUMBER,
        3: oracle.NATIVE_INT,
        8: oracle.LONG_STRING,  # LONG
        11: oracle.STRING,  # ROWID
        12: oracle.DATETIME,
        23: oracle.BINARY,
        24: oracle.LONG_BINARY,
        96: oracle.STRING,  # FIXED_CHAR
        112: oracle.STRING,  # CLOB
        113: oracle.BLOB,
        180: oracle.TIMESTAMP,
        252: oracle.BOOLEAN,
    }

    try:
        object_type = plsql_types[plsql_type.datatype]
    except KeyError:
        # nested table # varray # plsql record # plsql table
        if plsql_type.datatype not in {122, 123, 250, 251}:
            raise

        object_type = plsql._connection.gettype(
            type_name(plsql=plsql, resolved=resolved, plsql_type=plsql_type)
        )

        return (
            object_type,
            UserVar(make_in_converter(object_type)),
        )
    else:
        return object_type, SimpleVar(cursor, object_type)


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


def search_object(
    plsql: Database, name: ResolvedName, item: str
) -> Optional[Union[Subprogram, Package]]:
    if name.object_type in {
        ObjectTypes.function,
        ObjectTypes.procedure,
    }:
        return Subprogram(
            plsql=plsql, resolved=name, arguments=plsql._describe_procedure(item),
        )
    elif name.object_type == ObjectTypes.package:
        items = item.split(".")
        with_schema = plsql.is_schema(items[0])
        if len(items) == 3 and with_schema or len(items) == 2 and not with_schema:
            return Subprogram(
                plsql=plsql, resolved=name, arguments=plsql._describe_procedure(item),
            )
        return Package(plsql=plsql, name=item)


class Database:
    def __init__(
        self,
        user: str,
        password: str,
        service_auth: Tuple[str, int, str],
        encoding: str,
    ):
        host, port, service_name = service_auth

        dsn = oracle.makedsn(host, port, service_name=service_name)
        self._connection = oracle.connect(
            user=user, password=password, dsn=dsn, encoding=encoding, nencoding=encoding
        )

    def is_schema(self, schema_name: str) -> bool:
        return bool(
            self.query(
                """SELECT COUNT(*) FROM all_users WHERE username = UPPER(:username)""",
                username=schema_name,
            ).first
        )

    def __getattr__(self, item) -> Union[Schema, Package, Subprogram]:
        try:
            name = self._name_resolve(item)
        except (oracle.DatabaseError, NotFound):
            if self.is_schema(schema_name=item):
                return Schema(plsql=self, name=item)
            raise NotFound
        else:
            if found_object := search_object(plsql=self, name=name, item=item):
                return found_object

        raise AttributeError

    def _describe_procedure(self, name: str) -> Iterator[Argument]:
        arguments = _dbms_describe_describe_procedure(self._connection, name)

        return (Argument(*argument) for argument in arguments)

    def _name_resolve(self, name: str) -> ResolvedName:
        """Resolves name using in-built database procedure DBMS_UTILITY.NAME_RESOLVE"""
        (
            schema,
            part1,
            part2,
            database_link,
            part1_type,
            object_id,
        ) = _exhaustive_name_resolution(connection=self._connection, name=name)

        object_type = ObjectTypes(part1_type)

        if object_type == ObjectTypes.package and part2:
            subprogram_id = self.query(
                """
            SELECT subprogram_id
              FROM all_procedures
             WHERE object_id = :object_id
               AND procedure_name = :procedure_name
            """,
                object_id=object_id,
                procedure_name=part2,
            ).first
        else:
            subprogram_id = None

        return ResolvedName(
            schema,
            ".".join([part1 or "", part2 or ""]).strip("."),
            database_link,
            object_type,
            object_id,
            subprogram_id,
        )

    def query(self, sql: str, *positional_binds, **named_binds) -> Query:
        return Query(self._connection, sql, *positional_binds, **named_binds)

    def execute(self, statement: str, *args, **kwargs) -> None:
        with self._connection.cursor() as cursor:
            cursor.execute(statement, *args, **kwargs)
