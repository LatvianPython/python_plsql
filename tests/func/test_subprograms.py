import pytest

from python_plsql import DatabaseError


def test_function_returns_value(plsql, simple_function):
    assert simple_function(21) == 42
    assert simple_function(p_int=21) == 42
    assert simple_function(None) is None


def test_procedure_gets_called(simple_procedure):
    with pytest.raises(DatabaseError, match="ORA-20001.+You called me.+42"):
        simple_procedure()


@pytest.mark.parametrize(
    "args, kwargs, expected",
    [(["aaa"], {}, "aaa"), ([], {"p_varchar": "aaa"}, "aaa"), ([None], {}, "NULL")],
)
def test_procedure_with_parameters(plsql, args, kwargs, expected):
    with pytest.raises(DatabaseError, match=f"ORA-20002.+p_varchar={expected}"):
        plsql.test_package.proc_with_params(*args, **kwargs)
