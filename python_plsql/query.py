from __future__ import annotations

from collections import namedtuple
from itertools import starmap
from operator import itemgetter

import oracledb as oracle


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

            yield from records

    @property
    def first(self):
        try:
            return next(self._execute())
        except StopIteration:
            return None

    def __iter__(self):
        return self._execute()
