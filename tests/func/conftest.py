import pytest
import itertools

import oracledb


def recurse_getattr(current, attributes):
    attributes = list(filter(None, attributes))
    if attributes:
        attribute, *attributes = attributes
        return recurse_getattr(getattr(current, attribute), attributes)
    return current


@pytest.fixture(
    params=map(
        ".".join,
        itertools.product(
            ["", "test_user"],
            [
                "simple_function",
                "test_package.simple_function",
                "synonym_function",
                "synonym_package.simple_function",
            ],
        ),
    )
)
def simple_function(plsql, request):
    return recurse_getattr(plsql, request.param.split("."))


@pytest.fixture(
    params=map(
        ".".join,
        itertools.product(
            ["", "test_user"],
            [
                "simple_procedure",
                "test_package.simple_procedure",
                "synonym_procedure",
                "synonym_package.simple_procedure",
            ],
        ),
    )
)
def simple_procedure(plsql, request):
    return recurse_getattr(plsql, request.param.split("."))


def pytest_configure(config):
    config.addinivalue_line(
        "markers", "xfail_thick(reason): expected to fail in oracledb thick mode"
    )


@pytest.fixture(autouse=True)
def xfail_thick(request, plsql):
    marker = request.node.get_closest_marker("xfail_thick")
    if marker and not oracledb.is_thin_mode():
        request.applymarker(pytest.mark.xfail(strict=True, **marker.kwargs))
