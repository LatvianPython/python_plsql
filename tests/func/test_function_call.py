import pytest
from functools import reduce


@pytest.fixture(params=["simple_function", "test_package.simple_function"])
def simple_function(plsql, request):
    for access in request.param.split("."):
        plsql = getattr(plsql, access)
    return plsql


def test_function_returns_value(plsql, simple_function):
    assert simple_function(21) == 42
    assert simple_function(p_int=21) == 42
    assert simple_function(None) is None
