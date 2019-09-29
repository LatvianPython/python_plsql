from collections import namedtuple

import cx_Oracle as oracle

# class Schema:
#     sql_query = '''
# SELECT COUNT(*)
#   FROM all_users
#  WHERE username = :name
# '''
#
#     def __init__(self, name, plsql):
#         self.name = name
#         self.plsql = plsql
#         result = list(plsql.query(sql_query=self.sql_query,
#                                   bind_variables={'name': name.upper()}))
#         if sum(row[0] for row in result) == 0:
#             raise ValueError('Not a database schema!')
# @lru_cache(maxsize=None)
# def get_schema(name, plsql):
#     try:
#         return Schema(name=name, plsql=plsql)
#     except ValueError:
#         return None
#
#
# class Package:
#     pass
#
#

TEST_SCHEMA = 'TEST_USER'
FUNCTION = 'FUNCTION'
PROCEDURE = 'PROCEDURE'


class Subprogram:
    subprogram_sql = f'''
SELECT object_type, object_name
  FROM all_procedures
 WHERE owner = UPPER(:owner)
   AND object_name = UPPER(:name)
'''

    argument_sql = f'''
SELECT argument_name, data_type, defaulted, in_out
  FROM all_arguments
 WHERE owner = UPPER(:owner)
   AND object_name = UPPER(:name)
'''

    argument_mapping = {
        'VARCHAR2': str,
        'INTEGER': int,
        'NUMBER': float
    }

    def __init__(self, name, plsql):
        self.name, self.plsql = name, plsql

        if '.' in name:
            schema, name = name.split('.')

        binds = {'owner': TEST_SCHEMA, 'name': name}
        self.definition = plsql.query(sql_query=self.subprogram_sql, bind_variables=binds).first

        binds = {'owner': TEST_SCHEMA, 'name': name}
        self.arguments = [
            argument
            for argument
            in plsql.query(sql_query=self.argument_sql, bind_variables=binds).all
        ]

        if self.definition.object_type == FUNCTION:
            self.return_type = next(
                self.argument_mapping[argument.data_type]
                for argument
                in self.arguments
                if argument.argument_name is None
            )

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

            if self.definition.object_type == FUNCTION:
                result = cursor.callfunc(self.name, self.return_type, keywordParameters=kwargs)

                if in_out_parameters:
                    return result, {
                        name: parameter.getvalue()
                        for name, parameter
                        in in_out_parameters
                    }
                return result
            elif self.definition.object_type == PROCEDURE:
                cursor.callproc(self.name, keywordParameters=kwargs)

                if in_out_parameters:
                    return {
                        name: parameter.getvalue()
                        for name, parameter
                        in in_out_parameters
                    }
            else:
                raise NotImplementedError(f'Unrecognized object_type "{self.definition.object_type}"!')


class AttributeWalker:
    def __init__(self, plsql, attr):
        self.plsql, self.attr = plsql, [attr]

    def __getattr__(self, item):
        self.attr.append(item)
        return self

    def __call__(self, **kwargs):
        subprogram = Subprogram('.'.join(self.attr), self.plsql)
        return subprogram(**kwargs)


class Query:

    def __init__(self, connection, query, binds):
        self.connection, self.query, self.binds = connection, query, binds

    def execute(self):
        with self.connection.cursor() as cursor:
            cursor.execute(self.query, self.binds)
            Result = namedtuple('Result', [column[0].lower() for column in cursor.description])
            for rec in cursor:
                yield Result(*rec)

    @property
    def first(self):
        first_row = next(self.execute())
        if len(first_row) == 1:
            return first_row[0]
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
