import pytest
import datetime


@pytest.mark.parametrize(
    "func, expected",
    [
        ("ret_varchar", "42"),
        ("ret_number", 42.42),
        ("ret_binary_integer", 42),
        ("ret_clob", "42"),
        ("ret_rowid", "AAAACPAABAAAAShAAA"),
        ("ret_date", datetime.datetime(year=2019, month=12, day=20)),
        ("ret_raw", b"42"),
        ("ret_long_raw", b"42"),
        ("ret_char", "42"),
        ("ret_bool", True),
    ],
)
def test_return_values(plsql, func, expected):
    return_value = getattr(plsql.test_return, func)()

    assert return_value == expected
