import cx_Oracle as oracle
from collections import namedtuple
from functools import lru_cache


class Schema:
    sql_query = '''
SELECT COUNT(*)
  FROM all_users
 WHERE username = :name
'''

    def __init__(self, name, plsql):
        self.name = name
        self.plsql = plsql
        result = list(plsql.query(sql_query=self.sql_query,
                                  bind_variables={'name': name.upper()}))
        if sum(row[0] for row in result) == 0:
            raise ValueError('Not a database schema!')


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


class Subprogram:
    ArgumentRecord = namedtuple('ArgumentRecord', 'argument_name, data_type, defaulted, in_out')
    SubprogramRecord = namedtuple('SubprogramRecord', 'object_type, object_name')

    subprogram_sql = f'''
SELECT {','.join(ArgumentRecord._fields)}
  FROM all_procedures
 WHERE owner = UPPER(:owner)
   AND object_name = UPPER(:name)
'''

    argument_sql = f'''
SELECT {','.join(ArgumentRecord._fields)}
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

        binds = {'owner': TEST_SCHEMA, 'name': name.upper()}
        self.arguments = (
            self.ArgumentRecord(*argument)
            for argument
            in plsql.query(sql_query=self.argument_sql, bind_variables=binds)
        )

        self.return_type = next(
            self.argument_mapping[argument.data_type]
            for argument
            in self.arguments
        )

    def __call__(self, *args, **kwargs):
        with self.plsql.connection.cursor() as cursor:
            return cursor.callfunc(self.name, self.return_type, keywordParameters=kwargs)


class Database:

    def __init__(self, user, password, host, port, service_name, encoding):
        dsn = oracle.makedsn(host, port, service_name=service_name)
        self.connection = oracle.connect(user=user, password=password, dsn=dsn, encoding=encoding, nencoding=encoding)

    def execute_immediate(self, dynamic_string):
        with self.connection.cursor() as cursor:
            cursor.execute(dynamic_string)

    def query(self, sql_query, bind_variables):
        with self.connection.cursor() as cursor:
            cursor.execute(sql_query, bind_variables)
            yield from cursor

    def __getattr__(self, item):
        return Subprogram(item, self)
