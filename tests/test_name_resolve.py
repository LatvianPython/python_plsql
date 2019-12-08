import pytest

from plsql import DatabaseError


@pytest.mark.parametrize(
    "name,expected",
    [
        ("simple_procedure", ("TEST_USER", "SIMPLE_PROCEDURE", "PROCEDURE")),
        ("simple_function", ("TEST_USER", "SIMPLE_FUNCTION", "FUNCTION")),
        ("test_package", ("TEST_USER", "TEST_PACKAGE", "PACKAGE")),
        (
            "test_package.simple_procedure",
            ("TEST_USER", "TEST_PACKAGE.SIMPLE_PROCEDURE", "PACKAGE"),
        ),
        ("test_table", ("TEST_USER", "TEST_TABLE", "TABLE"),),
        ("test_sequence", ("TEST_USER", "TEST_SEQUENCE", "SEQUENCE"),),
        ("test_type", ("TEST_USER", "TEST_TYPE", "TYPE"),),
        ("test_synonym_procedure", ("TEST_USER", "SIMPLE_PROCEDURE", "PROCEDURE"),),
        ("test_synonym_function", ("TEST_USER", "SIMPLE_FUNCTION", "FUNCTION"),),
    ],
)
def test_names_are_resolved(plsql, name, expected):
    assert plsql._name_resolve(name) == expected


def test_nonexistent_name_raises_error(plsql):
    with pytest.raises(DatabaseError, match="ORA-06564"):
        plsql._name_resolve("aoeuqjkxpyfglrcgsnthzvwm")
