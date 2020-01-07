import pytest
import datetime

IN_RECORD = (42, 84, 126)
IN_VARRAY = list(range(10, 0, -1))
IN_NESTED = [i * 2 for i in range(1, 11)]
IN_PLSQL_TABLE = {i: i for i in range(1, 11)}

OUT_RECORD = (42, 84, 126)
OUT_VARRAY = list(range(10, 0, -1))
OUT_NESTED = [i * 2 for i in range(1, 11)]
OUT_PLSQL_TABLE = {i: i for i in range(1, 11)}


@pytest.mark.parametrize(
    "func, in_value, out_value",
    [
        ("io_varchar2", "42", "42"),
        ("io_varchar", "42", "42"),
        ("io_string", "42", "42"),
        ("io_number", 42.42, 42.42),
        ("io_integer", 42.0, 42.0),
        ("io_smallint", 42.0, 42.0),
        ("io_real", 42.42, 42.42),
        ("io_float", 42.42, 42.42),
        ("io_numeric", 42.0, 42.0),
        ("io_decimal", 42.0, 42.0),
        ("io_binary_integer", 42, 42),
        ("io_pls_integer", 42, 42),
        ("io_positive", 42, 42),
        ("io_natural", 42, 42),
        ("io_clob", "42", "42"),
        ("io_long", "42", "42"),
        ("io_rowid", "AAAACPAABAAAAShAAA", "AAAACPAABAAAAShAAA"),
        (
            "io_date",
            datetime.datetime(year=2019, month=12, day=20),
            datetime.datetime(year=2019, month=12, day=20),
        ),
        (
            "io_timestamp",
            datetime.datetime(year=2019, month=12, day=20),
            datetime.datetime(year=2019, month=12, day=20),
        ),
        ("io_raw", b"42", b"42"),
        ("io_long_raw", b"42", b"42"),
        ("io_char", "42".ljust(12000, " "), "42".ljust(12000, " ")),
        ("io_character", "42".ljust(12000, " "), "42".ljust(12000, " ")),
        ("io_bool", True, True),
        ("io_record", IN_RECORD, IN_RECORD),
        pytest.param(
            "io_record_of_records",
            (42, IN_RECORD, IN_RECORD),
            (42, IN_RECORD, IN_RECORD),
            marks=pytest.mark.skip(
                reason="OCI-21602: operation does not support the specified typecode"
            ),
        ),
        ("io_record_of_nested", (42, IN_NESTED, IN_NESTED), (42, IN_NESTED, IN_NESTED)),
        (
            "io_record_of_plsql_table",
            (42, IN_PLSQL_TABLE, IN_PLSQL_TABLE),
            (42, IN_PLSQL_TABLE, IN_PLSQL_TABLE),
        ),
        ("io_nested", IN_NESTED, IN_NESTED),
        ("io_nested_of_records", [IN_RECORD] * 10, [IN_RECORD] * 10),
        (
            "io_nested_of_record_of_nested",
            [(42, IN_NESTED, IN_NESTED)] * 10,
            [(42, IN_NESTED, IN_NESTED)] * 10,
        ),
        ("io_varray", IN_VARRAY, IN_VARRAY),
        ("io_plsql_table", IN_PLSQL_TABLE, IN_PLSQL_TABLE),
        (
            "io_plsql_table_of_records",
            {i: IN_RECORD for i in range(1, 11)},
            {i: IN_RECORD for i in range(1, 11)},
        ),
        pytest.param(
            "io_varray_of_plsql_table",
            [IN_PLSQL_TABLE] * 10,
            [IN_PLSQL_TABLE] * 10,
            marks=pytest.mark.skip("Memory access violation"),
        ),
        pytest.param(
            "io_varray_of_nested",
            [IN_NESTED] * 10,
            [IN_NESTED] * 10,
            marks=pytest.mark.skip("Memory access violation"),
        ),
        pytest.param(
            "io_plsql_table_of_nested",
            {i: IN_NESTED for i in range(1, 11)},
            {i: IN_NESTED for i in range(1, 11)},
            marks=pytest.mark.skip("Memory access violation"),
        ),
        pytest.param(
            "io_nested_of_nested",
            [IN_NESTED] * 10,
            [IN_NESTED] * 10,
            marks=pytest.mark.skip("Memory access violation"),
        ),
        pytest.param(
            "io_nested_of_plsql_table",
            [IN_PLSQL_TABLE] * 10,
            [IN_PLSQL_TABLE] * 10,
            marks=pytest.mark.skip("Memory access violation"),
        ),
        pytest.param(
            "io_plsql_table_of_plsql_table",
            {i: IN_PLSQL_TABLE for i in range(1, 11)},
            {i: IN_PLSQL_TABLE for i in range(1, 11)},
            marks=pytest.mark.skip("Memory access violation"),
        ),
    ],
)
def test_return_values(plsql, func, in_value, out_value):
    assert getattr(plsql.test_in_out_params, func)(in_value).p_param == out_value
