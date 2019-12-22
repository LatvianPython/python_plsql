import pytest
from python_plsql import DatabaseError, NotFound


def test_simple_procedure_gets_called(plsql):
    with pytest.raises(DatabaseError, match="You called me.+42"):
        plsql.test_package.simple_procedure()


def test_error_when_subprogram_does_not_exist(plsql):
    with pytest.raises(NotFound):
        plsql.test_package.aoeuidhtqjkxpyfg()
