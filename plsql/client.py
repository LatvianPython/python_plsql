from __future__ import annotations

import datetime
from collections import namedtuple
from itertools import starmap, chain
from operator import itemgetter

import cx_Oracle as oracle

FUNCTION = "FUNCTION"
PROCEDURE = "PROCEDURE"
PACKAGE = "PACKAGE"


def parse_in_out(parameters):
    return {
        param_name: param_value.getvalue() for param_name, param_value in parameters
    }


def oracle_plsql_record(connection, argument, mapping, record_type=None):
    if record_type is None:
        record_type = connection.gettype(argument.extended_type.upper())
    record = record_type.newobject()

    for key, value in mapping.items():
        setattr(record, key.upper(), value)
    return record


def oracle_plsql_table(connection, argument, mapping_of_recs):
    table_type = connection.gettype(argument.extended_type)
    table = table_type.newobject()

    if table_type.elementType is not None:
        for key, value in mapping_of_recs.items():
            rec = oracle_plsql_record(connection, None, value, table_type.elementType)
            table.setelement(key, rec)
        return table

    return mapping_of_recs


def translate_types(connection, arguments, parameters, conversion_func, data_type):
    return {
        argument.argument_name.lower(): conversion_func(
            connection, argument, parameters[argument.argument_name.lower()]
        )
        for argument in arguments
        if "IN" in argument.in_out
        if argument.data_type == data_type
    }


class Subprogram:
    argument_sql = """
SELECT argument_name, 
       data_type,
       defaulted, 
       in_out, 
       type_owner || '.' || type_name || '.' || type_subname extended_type
  FROM all_arguments
 WHERE owner = UPPER(:owner)
   AND object_name = :object_name
   AND object_id = :object_id 
   AND subprogram_id = :subprogram_id
"""

    # fixme: not gonna scale with other types
    argument_mapping = {
        "VARCHAR2": str,
        "INTEGER": int,
        "NUMBER": float,
        "DATE": datetime.datetime,
        "CLOB": oracle.CLOB,
        "BLOB": oracle.BLOB,
    }

    def __init__(self, plsql, name, definition):
        self.plsql = plsql
        self.name = name
        self.definition = definition

        binds = {
            "owner": self.definition.owner,
            "object_name": self.definition.object_name,
            "object_id": self.definition.object_id,
            "subprogram_id": self.definition.subprogram_id,
        }
        self.arguments = list(plsql.query(sql_query=self.argument_sql, binds=binds))

        try:
            return_argument = next(
                argument
                for argument in self.arguments
                if argument.argument_name is None
            )
        except StopIteration:
            self.return_type = None
        else:
            try:
                self.return_type = self.argument_mapping[return_argument.data_type]
            except KeyError:
                self.return_type = plsql.connection.gettype(
                    return_argument.extended_type
                )

    def __call__(self, **kwargs):
        with self.plsql.connection.cursor() as cursor:

            in_out_parameters = [
                (
                    argument.argument_name.lower(),
                    cursor.var(self.argument_mapping[argument.data_type]),
                )
                for argument in self.arguments
                if "OUT" in argument.in_out
                if argument.argument_name is not None
            ]

            for name, parameter in in_out_parameters:
                try:
                    parameter.setvalue(0, kwargs[name])
                except KeyError:
                    pass
                kwargs[name] = parameter

            object_type = self.definition.object_type

            if object_type == PACKAGE:
                if self.return_type:
                    object_type = FUNCTION
                else:
                    object_type = PROCEDURE

            translated_types = chain.from_iterable(
                translate_types(
                    self.plsql.connection, self.arguments, kwargs, func, data_type
                ).items()
                for func, data_type in [
                    (oracle_plsql_record, "PL/SQL RECORD"),
                    (oracle_plsql_table, "PL/SQL TABLE"),
                ]
            )

            for argument_name, argument_value in translated_types:
                kwargs[argument_name] = argument_value

            if object_type == FUNCTION:
                result = cursor.callfunc(
                    self.name, self.return_type, keywordParameters=kwargs
                )

                try:
                    attributes = result.type.attributes

                    if result.type.iscollection:
                        result_list = result.aslist()

                        try:
                            attributes = result_list[0].type.attributes
                        except IndexError:
                            result = []
                        except AttributeError:
                            result = result_list
                        else:
                            result = [
                                {
                                    attribute.name.lower(): getattr(
                                        item, attribute.name
                                    )
                                    for attribute in attributes
                                }
                                for item in result_list
                            ]
                    else:
                        result = {
                            attribute.name.lower(): getattr(result, attribute.name)
                            for attribute in attributes
                        }
                except AttributeError:
                    pass

                if in_out_parameters:
                    return result, parse_in_out(in_out_parameters)
                return result
            elif object_type == PROCEDURE:
                cursor.callproc(self.name, keywordParameters=kwargs)

                if in_out_parameters:
                    return parse_in_out(in_out_parameters)
            else:
                raise NotImplementedError(f'Unrecognized object_type "{object_type}"!')


def retrieve_subprograms(attributes, plsql):
    attribute_len = len(attributes)

    base_query = """
SELECT owner, 
       object_id, 
       subprogram_id, 
       NVL(procedure_name, object_name) object_name, 
       object_type
  FROM all_procedures
 WHERE object_type IN ('FUNCTION', 'PROCEDURE', 'PACKAGE') AND {extra_where_predicates}
"""

    def query_subprograms(**kwargs):
        extra_where_predicates = (f"{key} = UPPER(:{key})" for key in kwargs.keys())
        query_sql = base_query.format(
            extra_where_predicates=" AND ".join(extra_where_predicates)
        )
        return list(plsql.query(query_sql, binds=kwargs))

    if attribute_len == 3:
        owner, object_name, procedure_name = attributes
        return query_subprograms(
            owner=owner, object_name=object_name, procedure_name=procedure_name
        )
    elif attribute_len == 2:
        object_name, procedure_name = attributes

        matching_subprograms = query_subprograms(
            object_name=object_name, procedure_name=procedure_name
        )

        if not matching_subprograms:
            return query_subprograms(owner=object_name, object_name=procedure_name)
        return matching_subprograms
    else:
        (object_name,) = attributes
        return query_subprograms(object_name=object_name)


def match_parameters(subprograms, parameters, plsql):
    # fixme: this sql is essentially the same as in when building the Subprogram
    argument_sql = """
SELECT argument_name, 
       data_type, 
       defaulted, 
       in_out, 
       type_owner || '.' || type_name || '.' || type_subname extended_type
  FROM all_arguments
 WHERE owner = UPPER(:owner)
   AND object_name = :object_name
   AND object_id = :object_id 
   AND subprogram_id = :subprogram_id
"""

    for subprogram in subprograms:
        binds = {
            "owner": subprogram.owner,
            "object_name": subprogram.object_name,
            "object_id": subprogram.object_id,
            "subprogram_id": subprogram.subprogram_id,
        }

        arguments = list(
            argument.argument_name.lower()
            for argument in plsql.query(sql_query=argument_sql, binds=binds)
            if argument.argument_name is not None
        )

        if set(arguments) == set(parameters.keys()):
            return subprogram


def resolve_subprogram(attributes, parameters, plsql):
    assert attributes, "Attributes should not be empty!"

    matching_subprograms = retrieve_subprograms(attributes, plsql)

    if not matching_subprograms:
        raise AttributeError("No such subprogram exists!")

    if len(matching_subprograms) > 1:
        matched = match_parameters(matching_subprograms, parameters, plsql)

        if matched:
            return matched
        raise NotImplementedError("Can not resolve to single subprogram!")

    return matching_subprograms[0]


class AttributeWalker:
    def __init__(self, plsql, attr):
        self.plsql, self.attributes = plsql, [attr]

    def __getattr__(self, item):
        if len(self.attributes) >= 3:
            raise ValueError(
                "Attribute access is too deep, maximum of 3 allowed! (schema, package, subprogram)"
            )

        self.attributes.append(item)
        return self

    def __call__(self, **parameters):
        found_subprogram = resolve_subprogram(
            attributes=self.attributes, parameters=parameters, plsql=self.plsql
        )
        subprogram = Subprogram(self.plsql, ".".join(self.attributes), found_subprogram)
        return subprogram(**parameters)


class Query:
    def __init__(self, connection, query, binds):
        self.connection, self.query, self.binds = connection, query, binds

    def execute(self):
        with self.connection.cursor() as cursor:
            if self.binds:
                cursor.execute(self.query, self.binds)
            else:
                cursor.execute(self.query)

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
        first_row = next(self.execute())
        return first_row

    def __iter__(self):
        return self.execute()


class Database:
    def __init__(
        self,
        user: str,
        password: str,
        host: str,
        port: int,
        service_name: str,
        encoding: str,
    ):
        dsn = oracle.makedsn(host, port, service_name=service_name)
        self.connection = oracle.connect(
            user=user, password=password, dsn=dsn, encoding=encoding, nencoding=encoding
        )

    def execute_immediate(self, dynamic_string: str):
        with self.connection.cursor() as cursor:
            cursor.execute(dynamic_string)

    def query(self, sql_query: str, binds=None):
        return Query(self.connection, sql_query, binds)

    def __getattr__(self, item):
        return AttributeWalker(self, item)
