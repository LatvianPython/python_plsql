import cx_Oracle as oracle


class Database:

    def __init__(self, user, password, host, port, service_name, encoding):
        dsn = oracle.makedsn(host, port, service_name=service_name)
        self.connection = oracle.connect(user=user, password=password, dsn=dsn, encoding=encoding, nencoding=encoding)

    def execute_immediate(self, dynamic_string):
        with self.connection.cursor() as cursor:
            cursor.execute(dynamic_string)

    def __getattr__(self, item):
        def func(**kwargs):
            with self.connection.cursor() as cursor:
                return cursor.callfunc(item, int, keywordParameters=kwargs)

        return func
