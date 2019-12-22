import pytest

from python_plsql import DatabaseError, NotFound


@pytest.mark.parametrize(
    "name,expected",
    [
        ("simple_procedure", ("TEST_USER", "SIMPLE_PROCEDURE")),
        ("simple_function", ("TEST_USER", "SIMPLE_FUNCTION")),
        ("test_package", ("TEST_USER", "TEST_PACKAGE")),
        ("test_package", ("TEST_USER", "TEST_PACKAGE"),),
        ("test_table", ("TEST_USER", "TEST_TABLE"),),
        ("test_sequence", ("TEST_USER", "TEST_SEQUENCE"),),
        ("test_type", ("TEST_USER", "TEST_TYPE"),),
        ("synonym_procedure", ("TEST_USER", "SIMPLE_PROCEDURE"),),
        ("synonym_function", ("TEST_USER", "SIMPLE_FUNCTION"),),
    ],
)
def test_names_are_resolved(plsql, name, expected):
    resolved = plsql._name_resolve(name=name)
    assert (resolved.schema, resolved.name) == expected


def test_nonexistent_name_raises_error(plsql):
    with pytest.raises(NotFound):
        plsql._name_resolve(name="aoeuqjkxpyfglrcgsnthzvwm")
