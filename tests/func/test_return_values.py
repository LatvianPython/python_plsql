import pytest
import datetime

RECORD = (42, 84, 126)
VARRAY = list(range(10, 0, -1))
NESTED = [i * 2 for i in range(1, 11)]
PLSQL_TABLE = {i: i for i in range(1, 11)}


@pytest.mark.parametrize(
    "func, expected",
    [
        ("ret_varchar2", "42"),
        ("ret_varchar", "42"),
        ("ret_string", "42"),
        ("ret_number", 42.42),
        ("ret_integer", 42.0),
        ("ret_smallint", 42.0),
        ("ret_real", 42.42),
        ("ret_float", 42.42),
        ("ret_numeric", 42.0),
        ("ret_decimal", 42.0),
        ("ret_binary_integer", 42),
        ("ret_pls_integer", 42),
        ("ret_positive", 42),
        ("ret_natural", 42),
        ("ret_clob", "42"),
        ("ret_long", "42"),
        ("ret_rowid", "AAAACPAABAAAAShAAA"),
        ("ret_date", datetime.datetime(year=2019, month=12, day=20)),
        ("ret_timestamp", datetime.datetime(year=2019, month=12, day=20)),
        ("ret_raw", b"42"),
        ("ret_long_raw", b"42"),
        ("ret_char", "42"),
        ("ret_character", "42"),
        ("ret_bool", True),
        ("ret_record", RECORD),
        ("ret_record_of_records", (42, RECORD, RECORD)),
        ("ret_record_of_nested", (42, NESTED, NESTED)),
        pytest.param(
            "ret_record_of_plsql_table",
            (42, PLSQL_TABLE, PLSQL_TABLE),
            marks=pytest.mark.xfail(reason="can't tell between NESTED/PLSQL tables"),
        ),
        ("ret_nested", NESTED),
        ("ret_nested_of_records", [RECORD] * 10),
        ("ret_nested_of_record_of_nested", [(42, NESTED, NESTED)] * 10),
        ("ret_varray", VARRAY),
        ("ret_plsql_table", PLSQL_TABLE),
        ("ret_plsql_table_of_records", {i: RECORD for i in range(1, 11)}),
        pytest.param(
            "ret_varray_of_plsql_table",
            [PLSQL_TABLE] * 10,
            marks=[
                pytest.mark.skip(reason="Memory access violation"),
                pytest.mark.xfail(reason="can't tell between NESTED/PLSQL tables"),
            ],
        ),
        pytest.param(
            "ret_varray_of_nested",
            [NESTED] * 10,
            marks=pytest.mark.skip(reason="Memory access violation"),
        ),
        pytest.param(
            "ret_plsql_table_of_nested",
            {i: NESTED for i in range(1, 11)},
            marks=pytest.mark.skip(reason="Memory access violation"),
        ),
        pytest.param(
            "ret_nested_of_nested",
            [NESTED] * 10,
            marks=pytest.mark.skip(reason="Memory access violation"),
        ),
        pytest.param(
            "ret_nested_of_plsql_table",
            [PLSQL_TABLE] * 10,
            marks=pytest.mark.skip(reason="Memory access violation"),
        ),
        pytest.param(
            "ret_plsql_table_of_plsql_table",
            {i: PLSQL_TABLE for i in range(1, 11)},
            marks=pytest.mark.skip(reason="Memory access violation"),
        ),
    ],
)
def test_return_values(plsql, func, expected):
    return_value = getattr(plsql.test_return, func)()

    assert return_value == expected
