import configparser
from pathlib import Path

import pytest

from plsql import Database

from cx_Oracle import DatabaseError


@pytest.fixture(scope="session")
def plsql():
    config = configparser.ConfigParser()
    config.read("./database.ini")

    parameters = dict(config["database"].items())

    user, password, encoding = (
        parameters["user"],
        parameters["password"],
        parameters["encoding"],
    )

    auth = (
        parameters["host"],
        parameters["port"],
        parameters["service_name"],
    )

    database = Database(
        user=user, password=password, service_auth=auth, encoding=encoding
    )

    directories = [
        directory for directory in Path(".").glob("./sql/*/") if directory.is_dir()
    ]

    objects = [
        (file, directory)
        for directory in directories
        for file in directory.glob("*.sql")
    ]

    create_objects(database, objects)

    yield database

    drop_all_objects(database, objects)


def create_objects(plsql, objects):
    for file_path, _ in objects:
        with open(file_path, mode="r", encoding="utf8") as file:
            sql_text = file.read()
        try:
            plsql.execute(sql_text)
        except DatabaseError as err:
            if err.args[0].code == 955:
                pass
            raise


def drop_all_objects(plsql, objects):
    def clean_name(name):
        if "-" in name:
            return name[: name.find("-")]
        return name

    objects = {(clean_name(file.stem), directory.name) for file, directory in objects}

    for object_name, object_type in objects:
        plsql.execute(f"DROP {object_type} {object_name}")
