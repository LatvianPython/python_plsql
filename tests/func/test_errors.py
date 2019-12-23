import pytest

from python_plsql import NotFound


def test_error_when_object_does_not_exist(plsql):
    with pytest.raises(NotFound):
        plsql.aoeuidhtqjkxpyfg()


def test_error_when_subprogram_does_not_exist(plsql):
    with pytest.raises(NotFound):
        plsql.test_package.aoeuidhtqjkxpyfg()


@pytest.mark.parametrize(
    "args, kwargs", [([1], {}), ([], {"p_int": 5}), ([1], {"p_int": 5})],
)
def test_incorrect_call_raises_exception(simple_procedure, args, kwargs):
    with pytest.raises(ValueError, match="Arguments do not match subprogram"):
        simple_procedure(*args, **kwargs)
