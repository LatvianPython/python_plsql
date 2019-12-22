import pytest

from python_plsql import DatabaseError


def test_function_returns_value(plsql, simple_function):
    assert simple_function(21) == 42
    assert simple_function(p_int=21) == 42
    assert simple_function(None) is None


def test_procedure_gets_called(simple_procedure):
    with pytest.raises(DatabaseError, match="ORA-20001.+You called me.+42"):
        simple_procedure()
