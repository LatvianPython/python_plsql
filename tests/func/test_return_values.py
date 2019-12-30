import pytest
import datetime

RECORD = (42, 84, 126)
NESTED = [i * 2 for i in range(1, 11)]
PLSQL_TABLE = {i: i for i in range(1, 11)}


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
        ("ret_record", RECORD),
        ("ret_record_of_records", (42, RECORD, RECORD)),
        ("ret_record_of_nested", (42, NESTED, NESTED),),
        pytest.param(
            "ret_record_of_plsql_table",
            (42, PLSQL_TABLE, PLSQL_TABLE),
            marks=pytest.mark.xfail(
                reason="No current way to tell between NESTED and PLSQL tables for multi-layered types"
            ),
        ),
        ("ret_nested", NESTED),
        ("ret_nested_of_records", [RECORD] * 10),
        ("ret_nested_of_record_of_nested", [(42, NESTED, NESTED)] * 10),
        ("ret_plsql_table", PLSQL_TABLE),
        ("ret_plsql_table_of_records", {i: RECORD for i in range(1, 11)}),
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
