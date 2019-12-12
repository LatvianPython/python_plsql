from __future__ import annotations

from collections import namedtuple
from enum import IntEnum
from typing import Tuple, Iterator

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
                True,
            ],
        )

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


class Function:
    def __init__(self, name: ResolvedName):
        self._name = name


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

    def __getattr__(self, item):
        try:
            name = self._name_resolve(item)
        except oracle.DatabaseError:
            raise AttributeError

        if name.object_type == ObjectTypes.function:
            return Function(name)

        raise AttributeError

    def _describe_procedure(self, name: str) -> List[Argument]:
        result = _dbms_describe_describe_procedure(self._connection, name)

        return [Argument(*argument) for argument in result]

    def _name_resolve(self, name: str) -> ResolvedName:
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

    def query(self, sql: str, *args, **kwargs):
        pass

    def execute(self, statement: str, *args, **kwargs) -> None:
        with self._connection.cursor() as cursor:
            cursor.execute(statement, *args, **kwargs)
