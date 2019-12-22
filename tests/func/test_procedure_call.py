from python_plsql import DatabaseError, NotFound
import pytest


def test_simple_procedure_gets_called(plsql):
    with pytest.raises(DatabaseError, match="You called me.+42"):
        plsql.simple_procedure()


@pytest.mark.parametrize(
    "args, kwargs", [([1], {}), ([], {"p_int": 5}), ([1], {"p_int": 5})],
)
def test_incorrect_call_raises_exception(plsql, args, kwargs):
    with pytest.raises(ValueError, match="Arguments do not match subprogram"):
        plsql.simple_procedure(*args, **kwargs)


def test_error_when_subprogram_does_not_exist(plsql):
    with pytest.raises(NotFound):
        plsql.aoeuidhtqjkxpyfg()
