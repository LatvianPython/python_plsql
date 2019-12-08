from __future__ import annotations

from typing import Tuple
from collections import namedtuple

import cx_Oracle as oracle


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
) -> Tuple[str, str, str, int]:
    not_found_error = None
    for context in range(0, 10):
        try:
            (schema, part1, part2, _, part1_type, _,) = _dbms_utility_name_resolve(
                connection=connection, name=name, context=context
            )
        except oracle.DatabaseError as err:
            if (error_code := err.args[0].code) in (4047, 6564):
                if error_code == 6564:
                    not_found_error = err
                continue
            raise
        else:
            break
    else:
        raise not_found_error

    return schema, part1, part2, part1_type


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

    def _name_resolve(self, name: str):
        schema, part1, part2, part1_type = _exhaustive_name_resolution(
            connection=self._connection, name=name
        )

        type_mapping = {
            2: "TABLE",
            5: "SYNONYM",
            6: "SEQUENCE",
            7: "PROCEDURE",
            8: "FUNCTION",
            9: "PACKAGE",
            13: "TYPE",
        }
        ResolvedName = namedtuple("ResolvedName", "schema name object_type")

        return ResolvedName(
            schema,
            ".".join([part1 or "", part2 or ""]).strip("."),
            type_mapping[part1_type],
        )

    def execute(self, statement: str, *args, **kwargs):
        with self._connection.cursor() as cursor:
            cursor.execute(statement, *args, **kwargs)
