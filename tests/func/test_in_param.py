import pytest
import datetime

RECORD = (42, 84, 126)
VARRAY = list(range(10, 0, -1))
NESTED = [i * 2 for i in range(1, 11)]
PLSQL_TABLE = {i: i for i in range(1, 11)}


@pytest.mark.parametrize(
    "func, in_value",
    [
        ("in_varchar2", "42"),
        ("in_varchar", "42"),
        ("in_string", "42"),
        ("in_number", 42.42),
        ("in_integer", 42.0),
        ("in_smallint", 42.0),
        ("in_real", 42.42),
        ("in_float", 42.42),
        ("in_numeric", 42.0),
        ("in_decimal", 42.0),
        ("in_binary_integer", 42),
        ("in_pls_integer", 42),
        ("in_positive", 42),
        ("in_natural", 42),
        ("in_clob", "42"),
        ("in_long", "42"),
        ("in_rowid", "AAAACPAABAAAAShAAA"),
        ("in_date", datetime.datetime(year=2019, month=12, day=20)),
        ("in_timestamp", datetime.datetime(year=2019, month=12, day=20)),
        ("in_raw", b"42"),
        ("in_long_raw", b"42"),
        ("in_char", "42"),
        ("in_character", "42"),
        ("in_bool", True),
        ("in_record", RECORD),
        pytest.param(
            "in_record_of_records",
            (42, RECORD, RECORD),
            marks=pytest.mark.skip(
                reason="OCI-21602: operation does not support the specified typecode"
            ),
        ),
        ("in_record_of_nested", (42, NESTED, NESTED)),
        ("in_record_of_plsql_table", (42, PLSQL_TABLE, PLSQL_TABLE),),
        ("in_nested", NESTED),
        ("in_nested_of_records", [RECORD] * 10),
        ("in_nested_of_record_of_nested", [(42, NESTED, NESTED)] * 10),
        ("in_varray", VARRAY),
        ("in_plsql_table", PLSQL_TABLE),
        ("in_plsql_table_of_records", {i: RECORD for i in range(1, 11)}),
        pytest.param(
            "in_varray_of_plsql_table",
            [PLSQL_TABLE] * 10,
            marks=pytest.mark.skip(reason="Memory access violation"),
        ),
        pytest.param(
            "in_varray_of_nested",
            [NESTED] * 10,
            marks=pytest.mark.skip(reason="Memory access violation"),
        ),
        pytest.param(
            "in_plsql_table_of_nested",
            {i: NESTED for i in range(1, 11)},
            marks=pytest.mark.skip(reason="Memory access violation"),
        ),
        pytest.param(
            "in_nested_of_nested",
            [NESTED] * 10,
            marks=pytest.mark.skip(reason="Memory access violation"),
        ),
        pytest.param(
            "in_nested_of_plsql_table",
            [PLSQL_TABLE] * 10,
            marks=pytest.mark.skip(reason="Memory access violation"),
        ),
        pytest.param(
            "in_plsql_table_of_plsql_table",
            {i: PLSQL_TABLE for i in range(1, 11)},
            marks=pytest.mark.skip(reason="Memory access violation"),
        ),
    ],
)
def test_return_values(plsql, func, in_value):
    getattr(plsql.test_in_params, func)(in_value)
