from __future__ import annotations

from collections import namedtuple
from enum import IntEnum
from itertools import groupby
from itertools import starmap
from operator import attrgetter
from operator import itemgetter
from typing import Any
from typing import Iterator
from typing import List
from typing import Optional
from typing import Union
from typing import Tuple

import cx_Oracle as oracle

Argument = namedtuple(
    "Argument",
    "overload position level argument_name datatype default_value in_out length precision scale radix",
)

ResolvedName = namedtuple(
    "ResolvedName", "schema name database_link object_type object_number"
)


class ObjectTypes(IntEnum):
    table = 2
    synonym = 5
    sequence = 6
    procedure = 7
    function = 8
    package = 9
    type = 13


class NotFound(Exception):
    pass


def _dbms_describe_describe_procedure(
    connection: oracle.Connection, name: str
) -> Iterator[Tuple[Any, ...]]:
    """Wrapper for Oracle DBMS_DESCRIBE.DESCRIBE_PROCEDURE procedure"""

    number_table, varchar2_table = (
        connection.gettype("DBMS_DESCRIBE.NUMBER_TABLE"),
        connection.gettype("DBMS_DESCRIBE.VARCHAR2_TABLE"),
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
            in_out.aslist(),
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
        object_number = cursor.var(int)

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
                object_number,
            ],
        )

        return (
            schema.getvalue(),
            part1.getvalue(),
            part2.getvalue(),
            database_link.getvalue(),
            part1_type.getvalue(),
            object_number.getvalue(),
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
        return next(self._execute())

    def __iter__(self):
        return self._execute()


class Function:
    def __init__(self, plsql: Database, name: ResolvedName):
        self._plsql, self._name = plsql, name


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
            if argument.position and argument.datatype
        ]

    def match(self, *args, **kwargs) -> bool:
        return (len(args) + len(kwargs)) == len(self.arguments)

    @property
    def is_function(self) -> bool:
        return bool(self.return_type)


def group_by_overload(arguments: Iterator[Argument]) -> List[Overload]:
    return [
        Overload(arguments=grouped_arguments)
        for _, grouped_arguments in groupby(arguments, attrgetter("overload"))
    ] or [Overload(arguments=[])]


def filter_match(matches: Iterator[Overload]) -> Overload:
    matches = list(matches)
    if len(matches) > 1:
        raise ValueError("Arguments matched with too many subprograms")
    elif len(matches) == 0:
        raise ValueError("Arguments do not match subprogram")
    return matches[0]


class Subprogram:
    def __init__(
        self, plsql: Database, resolved: ResolvedName, arguments: Iterator[Argument]
    ):
        self.plsql, self.resolved, self.overloads = (
            plsql,
            resolved,
            group_by_overload(arguments=arguments),
        )

    def _call_function(self, *args, **kwargs):
        _ = filter_match(self._function_matches(*args, **kwargs))

        with self.plsql._connection.cursor() as cursor:
            return cursor.callfunc(self.resolved.name, int, args, kwargs)

    def _call_procedure(self, *args, **kwargs):
        _ = filter_match(self._procedure_matches(*args, **kwargs))

        with self.plsql._connection.cursor() as cursor:
            cursor.callproc(self.resolved.name, args, kwargs)

    def __call__(self, *args, **kwargs):
        if self.overloaded and self.is_function and self.is_procedure:
            raise NotImplementedError(
                "Subprogram is overloaded as a function and procedure, use _call_(procedure/function) method"
            )

        if self.is_function:
            return self._call_function(*args, **kwargs)
        else:
            return self._call_procedure(*args, **kwargs)

    def _function_matches(self, *args, **kwargs) -> Iterator[Overload]:
        return filter(lambda x: x.is_function, self._matches(*args, **kwargs))

    def _procedure_matches(self, *args, **kwargs) -> Iterator[Overload]:
        return filter(lambda x: not x.is_function, self._matches(*args, **kwargs))

    def _matches(self, *args, **kwargs) -> Iterator[Overload]:
        """returns overloads that match with provided parameters"""
        return (
            overload for overload in self.overloads if overload.match(*args, **kwargs)
        )

    @property
    def overloaded(self) -> bool:
        """returns true if exists multiple definitions of the same subprogram in a package
        only applicable for package procedures/functions where overloading is possible"""
        return len(self.overloads) > 1

    @property
    def is_function(self) -> bool:
        return any(overload.is_function for overload in self.overloads)

    @property
    def is_procedure(self) -> bool:
        return any(not overload.is_function for overload in self.overloads)

    @property
    def standalone(self) -> bool:
        """returns true if procedure/function is not part of a package"""
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
            raise
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
            object_number,
        ) = _exhaustive_name_resolution(connection=self._connection, name=name)

        return ResolvedName(
            schema,
            ".".join([part1 or "", part2 or ""]).strip("."),
            database_link,
            ObjectTypes(part1_type),
            object_number,
        )

    def query(self, sql: str, *positional_binds, **named_binds) -> Query:
        return Query(self._connection, sql, *positional_binds, **named_binds)

    def execute(self, statement: str, *args, **kwargs) -> None:
        with self._connection.cursor() as cursor:
            cursor.execute(statement, *args, **kwargs)
