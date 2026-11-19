import configparser
from pathlib import Path

import pytest
from oracledb import DatabaseError

from python_plsql import Database

TESTS_DIR = Path(__file__).resolve().parent


@pytest.fixture(scope="session")
def plsql():
    config = configparser.ConfigParser()
    config.read(TESTS_DIR / "database.ini")

    parameters = dict(config["database"].items())

    user, password = parameters["user"], parameters["password"]

    auth = (
        parameters["host"],
        parameters["port"],
        parameters["service_name"],
    )

    database = Database(
        user=user,
        password=password,
        service_auth=auth,
        oracle_client_dir=parameters.get("oracle_client_dir") or None,
    )

    directories = [
        directory for directory in TESTS_DIR.glob("sql/*/") if directory.is_dir()
    ]

    objects = [
        (file, directory)
        for directory in directories
        for file in directory.glob("*.sql")
    ]

    assert objects, "no objects found!"

    drop_all_objects(database, objects)
    create_objects(database, objects)
    database.execute(
        "BEGIN dbms_utility.compile_schema(USER, compile_all => FALSE); END;"
    )

    yield database


def create_objects(plsql, objects):
    for file_path, _ in objects:
        with open(file_path, encoding="utf8") as file:
            sql_text = file.read()
        try:
            plsql.execute(sql_text)
        except DatabaseError as err:
            if err.args[0].code == 955:
                continue
            raise


def drop_all_objects(plsql, objects):
    def clean_name(name):
        if "-" in name:
            return name[: name.find("-")]
        return name

    objects = {(clean_name(file.stem), directory.name) for file, directory in objects}

    for object_name, object_type in objects:
        try:
            plsql.execute(f"DROP {object_type} {object_name}")
        except DatabaseError as err:
            error_code = err.args[0].code
            if error_code in [1434, 2289, 4043, 942]:
                continue
            raise
