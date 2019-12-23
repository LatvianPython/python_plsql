import pytest


@pytest.fixture(
    params=[
        "ret_varchar",
        "ret_number",
        "ret_binary_integer",
        "ret_clob",
        "ret_rowid",
        "ret_date",
        "ret_raw",
        "ret_long_raw",
        "ret_char",
        "ret_bool",
    ]
)
def functions(plsql, request):
    return getattr(plsql.test_return, request.param)


def test_return_values(functions):
    assert functions() is None
