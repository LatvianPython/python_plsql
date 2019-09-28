import cx_Oracle as oracle
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


@lru_cache(maxsize=None)
def get_schema(name, plsql):
    try:
        return Schema(name=name, plsql=plsql)
    except ValueError:
        return None


class Package:
    pass


class Subprogram:
    pass


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
            for row in cursor:
                yield row

    def __getattr__(self, item):
        schema = get_schema(item, self)

        if schema:
            return schema

        def func(**kwargs):
            with self.connection.cursor() as cursor:
                return cursor.callfunc(item, int, keywordParameters=kwargs)

        return func
