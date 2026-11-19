from __future__ import annotations

from collections import namedtuple
from datetime import datetime
from typing import TYPE_CHECKING
from typing import Any

import oracledb as oracle

from .introspection import Argument
from .introspection import ResolvedName

if TYPE_CHECKING:
    from .database import Database


def plsql_record(attributes) -> Any:
    return namedtuple("Record", (attribute.name.lower() for attribute in attributes))


# noinspection PyTypeChecker
def to_python(value):
    if isinstance(value, oracle.DbObject):
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
    if object_type and not isinstance(object_type, oracle.DbType):
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


# values for is_list, thick mode does not accept None as an element
_PROBE_VALUES = {
    oracle.DB_TYPE_NUMBER: 0,
    oracle.DB_TYPE_BINARY_INTEGER: 0,
    oracle.DB_TYPE_BINARY_FLOAT: 0.0,
    oracle.DB_TYPE_BINARY_DOUBLE: 0.0,
    oracle.DB_TYPE_BOOLEAN: False,
    oracle.DB_TYPE_VARCHAR: "",
    oracle.DB_TYPE_NVARCHAR: "",
    oracle.DB_TYPE_CHAR: "",
    oracle.DB_TYPE_NCHAR: "",
    oracle.DB_TYPE_RAW: b"",
    oracle.DB_TYPE_DATE: datetime(2000, 1, 1),
    oracle.DB_TYPE_TIMESTAMP: datetime(2000, 1, 1),
    oracle.DB_TYPE_TIMESTAMP_TZ: datetime(2000, 1, 1),
    oracle.DB_TYPE_TIMESTAMP_LTZ: datetime(2000, 1, 1),
}


def _probe_value(element_type):
    if isinstance(element_type, oracle.DbObjectType):
        return element_type.newobject()
    return _PROBE_VALUES.get(element_type)


def is_list(object_type: oracle.DbObjectType) -> bool:
    # nested tables and varrays are lists, index-by tables are dicts
    obj = object_type.newobject()
    try:
        obj.setelement(5, _probe_value(object_type.element_type))
    except oracle.Error:
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


_PLSQL_TYPES = {
    1: oracle.DB_TYPE_VARCHAR,
    2: oracle.DB_TYPE_NUMBER,
    3: oracle.DB_TYPE_BINARY_INTEGER,
    8: oracle.DB_TYPE_LONG,  # LONG
    11: oracle.DB_TYPE_VARCHAR,  # ROWID
    12: oracle.DB_TYPE_DATE,
    23: oracle.DB_TYPE_RAW,
    24: oracle.DB_TYPE_LONG_RAW,
    96: oracle.DB_TYPE_VARCHAR,  # FIXED_CHAR
    112: oracle.DB_TYPE_VARCHAR,  # CLOB
    113: oracle.DB_TYPE_BLOB,
    180: oracle.DB_TYPE_TIMESTAMP,
    252: oracle.DB_TYPE_BOOLEAN,
}

# nested table # varray # plsql record # plsql table
_USER_DEFINED_TYPES = {122, 123, 250, 251}


def user_defined_type(
    plsql: Database, resolved: ResolvedName, plsql_type: Argument
) -> oracle.DbObjectType:
    key = (
        resolved.object_id,
        resolved.subprogram_id,
        plsql_type.overload,
        plsql_type.position,
    )

    try:
        return plsql._types[key]
    except KeyError:
        object_type = plsql._types[key] = plsql._connection.gettype(
            type_name(plsql=plsql, resolved=resolved, plsql_type=plsql_type)
        )
        return object_type


def cursor_var(
    plsql: Database, cursor: oracle.Cursor, resolved: ResolvedName, plsql_type: Argument
):
    try:
        object_type = _PLSQL_TYPES[plsql_type.datatype]
    except KeyError:
        if plsql_type.datatype not in _USER_DEFINED_TYPES:
            raise

        object_type = user_defined_type(plsql, resolved, plsql_type)

        return (
            object_type,
            UserVar(make_in_converter(object_type)),
        )
    else:
        return object_type, SimpleVar(cursor, object_type)
