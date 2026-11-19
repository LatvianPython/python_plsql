from __future__ import annotations

from typing import Any
from typing import Iterator

import oracledb as oracle

from .errors import NotFound
from .introspection import Argument
from .introspection import ObjectTypes
from .introspection import ResolvedName
from .introspection import _dbms_describe_describe_procedure
from .introspection import _exhaustive_name_resolution
from .query import Query
from .subprogram import Subprogram


class Schema:
    def __init__(self, plsql: Database, name: str):
        self._plsql, self._name = plsql, name

    def __getattr__(self, item: str) -> Subprogram | Package | None:
        if item.startswith("_"):
            raise AttributeError(item)

        item = f"{self._name}.{item}"
        return self._plsql._cached(
            item,
            lambda: search_object(
                plsql=self._plsql, name=self._plsql._name_resolve(item), item=item
            ),
        )


class Package:
    def __init__(self, plsql: Database, name: str):
        self._plsql, self._name = plsql, name

    def __getattr__(self, item: str) -> Subprogram:
        if item.startswith("_"):
            raise AttributeError(item)

        item = f"{self._name}.{item}"
        return self._plsql._cached(
            item,
            lambda: Subprogram(
                plsql=self._plsql,
                resolved=self._plsql._name_resolve(item),
                arguments=self._plsql._describe_procedure(item),
            ),
        )


def search_object(
    plsql: Database, name: ResolvedName, item: str
) -> Subprogram | Package | None:
    if name.object_type in {
        ObjectTypes.function,
        ObjectTypes.procedure,
    }:
        return Subprogram(
            plsql=plsql,
            resolved=name,
            arguments=plsql._describe_procedure(item),
        )
    elif name.object_type == ObjectTypes.package:
        items = item.split(".")
        with_schema = plsql.is_schema(items[0])
        if len(items) == 3 and with_schema or len(items) == 2 and not with_schema:
            return Subprogram(
                plsql=plsql,
                resolved=name,
                arguments=plsql._describe_procedure(item),
            )
        return Package(plsql=plsql, name=item)


class Database:
    def __init__(
        self,
        user: str | None = None,
        password: str | None = None,
        service_auth: tuple[str, int, str] | None = None,
        oracle_client_dir: str | None = None,
        connection: oracle.Connection | None = None,
    ):
        self._objects: dict[str, Any] = {}
        self._types: dict[tuple[Any, ...], oracle.DbObjectType] = {}

        # thin mode reads PLS_INTEGER collection elements as BOOLEAN, thick does not
        if oracle_client_dir:
            oracle.init_oracle_client(lib_dir=oracle_client_dir)

        self._owns_connection = connection is None

        if connection is None:
            if service_auth is None:
                raise ValueError("Either service_auth or connection is required")

            host, port, service_name = service_auth

            connection = oracle.connect(
                user=user,
                password=password,
                host=host,
                port=int(port),
                service_name=service_name,
            )

        self._connection = connection

    def __enter__(self) -> Database:
        return self

    def __exit__(self, *exc_info) -> None:
        self.close()

    def close(self) -> None:
        # a connection passed in by the caller stays open
        if self._owns_connection:
            self._connection.close()

    def clear_cache(self) -> None:
        self._objects.clear()
        self._types.clear()

    def _cached(self, item: str, factory):
        key = item.lower()

        try:
            return self._objects[key]
        except KeyError:
            found = factory()
            if found is not None:
                self._objects[key] = found
            return found

    def is_schema(self, schema_name: str) -> bool:
        return bool(
            self.query(
                """SELECT COUNT(*) FROM all_users WHERE username = UPPER(:username)""",
                username=schema_name,
            ).first
        )

    def __getattr__(self, item) -> Schema | Package | Subprogram:
        if item.startswith("_"):
            raise AttributeError(item)

        return self._cached(item, lambda: self._find(item))

    def _find(self, item: str) -> Schema | Package | Subprogram:
        try:
            name = self._name_resolve(item)
        except (oracle.DatabaseError, NotFound) as err:
            if self.is_schema(schema_name=item):
                return Schema(plsql=self, name=item)
            raise NotFound(f"name {item} not found") from err
        else:
            if found_object := search_object(plsql=self, name=name, item=item):
                return found_object

        raise AttributeError(f"{item} is not a schema, package or subprogram")

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
