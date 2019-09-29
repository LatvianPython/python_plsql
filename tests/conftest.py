import configparser
from pathlib import Path

import pytest

from plsql import Database


@pytest.fixture(scope='session')
def plsql():
    config = configparser.ConfigParser()
    config.read('./database.ini')

    parameters = dict(config['database'].items())

    database = Database(**parameters)

    directories = [directory for directory in Path('.').glob('./sql/*/') if directory.is_dir()]

    objects = [
        (file, directory)
        for directory in directories
        for file in directory.glob('*.sql')
    ]

    create_object(database, objects)

    yield database

    drop_all_objects(database, objects)


def create_object(plsql, objects):
    for file, _ in objects:
        with open(file, mode='r', encoding='utf8') as file:
            sql_text = file.read()
        plsql.execute_immediate(sql_text)


def drop_all_objects(plsql, objects):
    for file, directory in objects:
        object_type, object_name = directory.name, file.stem,
        plsql.execute_immediate(f'DROP {object_type} {object_name}')
