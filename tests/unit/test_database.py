import pytest

from python_plsql import Database


def test_private_names_are_not_looked_up_in_database(plsql):
    with pytest.raises(AttributeError):
        _ = plsql._aoeuidhtqjkxpyfg

    with pytest.raises(AttributeError):
        _ = plsql.test_package._aoeuidhtqjkxpyfg

    with pytest.raises(AttributeError):
        _ = plsql.test_user._aoeuidhtqjkxpyfg


def test_attribute_lookup_without_connection_does_not_recurse():
    database = Database.__new__(Database)

    with pytest.raises(AttributeError):
        _ = database._connection


def test_connection_or_service_auth_is_required():
    with pytest.raises(ValueError):
        Database(user="user", password="password")


def test_existing_connection_is_used_and_left_open(plsql):
    with Database(connection=plsql._connection) as database:
        assert database.simple_function(21) == 42

    assert plsql.query("SELECT 1 FROM dual").first == 1


@pytest.mark.parametrize(
    "path",
    [
        ["simple_function"],
        ["test_package"],
        ["test_package", "simple_function"],
        ["test_user"],
        ["test_user", "test_package", "simple_function"],
    ],
)
def test_found_objects_are_cached(plsql, path):
    def find():
        found = plsql
        for name in path:
            found = getattr(found, name)
        return found

    first = find()
    assert find() is first

    plsql.clear_cache()
    assert find() is not first


def test_user_defined_types_are_cached(plsql):
    plsql.clear_cache()

    nested = [i * 2 for i in range(1, 11)]

    plsql.test_in_params.in_nested(nested)
    assert len(plsql._types) == 1

    plsql.test_in_params.in_nested(nested)
    assert len(plsql._types) == 1
