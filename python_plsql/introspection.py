from __future__ import annotations

from collections import namedtuple
from enum import IntEnum
from typing import Any
from typing import Iterator
from typing import Tuple

import oracledb as oracle

from .errors import NotFound

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
                raise NotFound(f"subprogram {name} not found") from err
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

    raise NotFound(f"name {name} not found")
