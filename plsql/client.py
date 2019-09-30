import datetime
from collections import namedtuple
from operator import itemgetter

import cx_Oracle as oracle

FUNCTION = 'FUNCTION'
PROCEDURE = 'PROCEDURE'
PACKAGE = 'PACKAGE'


class Subprogram:
    argument_sql = f'''
SELECT argument_name, data_type, defaulted, in_out
  FROM all_arguments
 WHERE owner = UPPER(:owner)
   AND object_name = :object_name
   AND object_id = :object_id 
   AND subprogram_id = :subprogram_id
'''
    subprogram_sql = f'''
SELECT owner, NVL(procedure_name, object_name) object_name, object_type
  FROM all_procedures
 WHERE owner = UPPER(:owner)
   AND object_id = :object_id 
   AND subprogram_id = :subprogram_id
   AND object_type IN ('FUNCTION', 'PROCEDURE', 'PACKAGE')
'''
    # fixme: not gonna scale with user defined types in database
    argument_mapping = {
        'VARCHAR2': str,
        'INTEGER': int,
        'NUMBER': float,
        'DATE': datetime.datetime,
        'CLOB': oracle.CLOB,
        'BLOB': oracle.BLOB
    }

    def __init__(self, plsql, name, owner, object_id, subprogram_id):
        self.owner, self.object_id, self.subprogram_id = owner, object_id, subprogram_id
        self.plsql = plsql
        self.name = name

        binds = {'owner': self.owner, 'object_id': self.object_id, 'subprogram_id': self.subprogram_id}
        self.definition = plsql.query(sql_query=self.subprogram_sql, bind_variables=binds).first

        binds = {'owner': self.owner, 'object_name': self.definition.object_name,
                 'object_id': self.object_id, 'subprogram_id': self.subprogram_id}
        self.arguments = list(plsql.query(sql_query=self.argument_sql, bind_variables=binds).all)

        try:
            self.return_type = next(
                self.argument_mapping[argument.data_type]
                for argument
                in self.arguments
                if argument.argument_name is None
            )
        except StopIteration:
            self.return_type = None

    def __call__(self, **kwargs):
        with self.plsql.connection.cursor() as cursor:

            in_out_parameters = [
                (argument.argument_name.lower(), cursor.var(self.argument_mapping[argument.data_type]))
                for argument
                in self.arguments
                if 'OUT' in argument.in_out
                if argument.argument_name is not None
            ]

            for name, parameter in in_out_parameters:
                try:
                    parameter.setvalue(0, kwargs[name])
                except KeyError:
                    pass
                kwargs[name] = parameter

            def pythonize_value(value):
                try:
                    return value.read()
                except AttributeError:
                    return value

            def parse_in_out(parameters):
                return {
                    param_name: pythonize_value(param_value.getvalue())
                    for param_name, param_value
                    in parameters
                }

            object_type = self.definition.object_type

            if object_type == PACKAGE:
                if self.return_type:
                    object_type = FUNCTION
                else:
                    object_type = PROCEDURE

            if object_type == FUNCTION:
                result = cursor.callfunc(self.name, self.return_type, keywordParameters=kwargs)

                result = pythonize_value(result)

                if in_out_parameters:
                    return result, parse_in_out(in_out_parameters)
                return result
            elif object_type == PROCEDURE:
                cursor.callproc(self.name, keywordParameters=kwargs)

                if in_out_parameters:
                    return parse_in_out(in_out_parameters)
            else:
                raise NotImplementedError(f'Unrecognized object_type "{object_type}"!')


def resolve_subprogram(attributes, parameters, plsql):
    assert attributes, 'Attributes should not be empty!'

    attribute_len = len(attributes)
    if attribute_len > 3:
        raise ValueError('Attribute access is too deep, maximum of 3 allowed! (schema, package, subprogram)')

    if attribute_len == 3:
        # schema, package, subprogram = attributes
        raise NotImplementedError('Can not access with full path!')
    elif attribute_len == 2:
        # todo: at some point use to refine search due to possibility of overloaded subprograms in package
        _ = parameters

        # search for subprogram assuming package name is provided
        object_name, procedure_name = attributes
        subprogram_sql = f'''
        SELECT owner, object_id, subprogram_id
          FROM all_procedures
         WHERE object_name = UPPER(:name)
           AND procedure_name = UPPER(:procedure_name)
           AND object_type IN ('FUNCTION', 'PROCEDURE', 'PACKAGE')
        '''
        binds = {'name': object_name, 'procedure_name': procedure_name}
        matching_subprograms = list(plsql.query(subprogram_sql, binds).all)

        if len(matching_subprograms) > 1:
            raise NotImplementedError('Can not resolve to single subprogram!')

        # if fails then must be standalone and schema is provided
        if not matching_subprograms:
            subprogram_sql = f'''
            SELECT owner, object_id, subprogram_id
              FROM all_procedures
             WHERE owner = UPPER(:owner)
               AND object_name = UPPER(:name)
               AND object_type IN ('FUNCTION', 'PROCEDURE', 'PACKAGE')
            '''
            owner, object_name = attributes
            binds = {'owner': owner, 'name': object_name}
            matching_subprograms = list(plsql.query(subprogram_sql, binds).all)
            if len(matching_subprograms) > 1:
                raise NotImplementedError('Can not resolve to single subprogram!')

            if not matching_subprograms:
                raise AttributeError('No such subprogram exists!')
    else:
        subprogram_sql = f'''
        SELECT owner, object_id, subprogram_id
          FROM all_procedures
         WHERE object_name = UPPER(:name)
           AND object_type IN ('FUNCTION', 'PROCEDURE', 'PACKAGE')
        '''
        subprogram, = attributes

        matching_subprograms = list(plsql.query(subprogram_sql, {'name': subprogram}).all)

        if not matching_subprograms:
            raise AttributeError('No such subprogram exists!')

        if len(matching_subprograms) > 1:
            raise NotImplementedError('Can not resolve to single subprogram!')

    return matching_subprograms[0]


class AttributeWalker:
    def __init__(self, plsql, attr):
        self.plsql, self.attributes = plsql, [attr]

    def __getattr__(self, item):
        self.attributes.append(item)
        return self

    def __call__(self, **parameters):
        found_subprogram = resolve_subprogram(attributes=self.attributes, parameters=parameters, plsql=self.plsql)
        subprogram = Subprogram(self.plsql, '.'.join(self.attributes), **found_subprogram._asdict())
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
                record_type = namedtuple('Result', [column[0].lower() for column in cursor.description])

                def result(rec):
                    return record_type(*rec)
            else:
                result = itemgetter(0)

            for record in cursor:
                yield result(record)

    @property
    def first(self):
        first_row = next(self.execute())
        return first_row

    @property
    def all(self):
        return self.execute()


class Database:

    def __init__(self, user, password, host, port, service_name, encoding):
        dsn = oracle.makedsn(host, port, service_name=service_name)
        self.connection = oracle.connect(user=user, password=password, dsn=dsn, encoding=encoding, nencoding=encoding)

    def execute_immediate(self, dynamic_string):
        with self.connection.cursor() as cursor:
            cursor.execute(dynamic_string)

    def query(self, sql_query, bind_variables=None):
        return Query(self.connection, sql_query, bind_variables)

    def __getattr__(self, item):
        return AttributeWalker(self, item)
