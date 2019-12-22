import pytest


@pytest.fixture(params=["simple_function", "test_package.simple_function"])
def simple_function(plsql, request):
    return getattr(plsql, request.param)


@pytest.fixture(params=["simple_procedure", "test_package.simple_procedure"])
def simple_procedure(plsql, request):
    return getattr(plsql, request.param)
