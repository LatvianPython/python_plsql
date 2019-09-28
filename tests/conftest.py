import pytest
from plsql import Database
from contextlib import contextmanager
import configparser


@pytest.fixture(scope='session')
def plsql():
    config = configparser.ConfigParser()
    config.read('./database.ini')

    parameters = dict(config['database'].items())
    return Database(**parameters)


@contextmanager
def managed_object(plsql, object_type, object_name):
    with open(f'./sql/{object_type}/{object_name}.sql', mode='r', encoding='utf8') as file:
        sql_text = file.read()

    plsql.execute_immediate(sql_text)
    yield
    # plsql.execute_immediate(f'DROP {object_type} {object_name}')


@pytest.fixture(scope='module')
def simple_function(plsql):
    with managed_object(plsql, 'function', 'simple_function'):
        yield


@pytest.fixture(scope='module')
def function_with_defaults(plsql):
    with managed_object(plsql, 'function', 'function_with_defaults'):
        yield


@pytest.fixture(scope='module')
def string_function(plsql):
    with managed_object(plsql, 'function', 'string_function'):
        yield
