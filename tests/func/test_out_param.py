import pytest
import datetime

from tests.func import BlankPadded
from tests.func import DUAL_ROWID
from tests.func import resolve

RECORD = (42, 84, 126)
VARRAY = list(range(10, 0, -1))
NESTED = [i * 2 for i in range(1, 11)]
PLSQL_TABLE = {i: i for i in range(1, 11)}


@pytest.mark.parametrize(
    "func, out_value",
    [
        ("out_varchar2", "42"),
        ("out_varchar", "42"),
        ("out_string", "42"),
        ("out_number", 42.42),
        ("out_integer", 42.0),
        ("out_smallint", 42.0),
        ("out_real", 42.42),
        ("out_float", 42.42),
        ("out_numeric", 42.0),
        ("out_decimal", 42.0),
        ("out_binary_integer", 42),
        ("out_pls_integer", 42),
        ("out_positive", 42),
        ("out_natural", 42),
        ("out_clob", "42"),
        ("out_long", "42"),
        ("out_rowid", DUAL_ROWID),
        ("out_date", datetime.datetime(year=2019, month=12, day=20)),
        ("out_timestamp", datetime.datetime(year=2019, month=12, day=20)),
        ("out_raw", b"42"),
        ("out_long_raw", b"42"),
        ("out_char", BlankPadded("42")),
        ("out_character", BlankPadded("42")),
        ("out_bool", True),
        ("out_record", RECORD),
        ("out_record_of_records", (42, RECORD, RECORD)),
        ("out_record_of_nested", (42, NESTED, NESTED)),
        ("out_record_of_plsql_table", (42, PLSQL_TABLE, PLSQL_TABLE),),
        ("out_nested", NESTED),
        ("out_nested_of_records", [RECORD] * 10),
        ("out_nested_of_record_of_nested", [(42, NESTED, NESTED)] * 10),
        ("out_varray", VARRAY),
        ("out_plsql_table", PLSQL_TABLE),
        ("out_plsql_table_of_records", {i: RECORD for i in range(1, 11)}),
        ("out_varray_of_plsql_table", [PLSQL_TABLE] * 10),
        ("out_varray_of_nested", [NESTED] * 10),
        ("out_plsql_table_of_nested", {i: NESTED for i in range(1, 11)}),
        ("out_nested_of_nested", [NESTED] * 10),
        ("out_nested_of_plsql_table", [PLSQL_TABLE] * 10),
        ("out_plsql_table_of_plsql_table", {i: PLSQL_TABLE for i in range(1, 11)}),
    ],
)
def test_return_values(plsql, func, out_value):
    result = getattr(plsql.test_out_params, func)(None)
    assert result.p_param == resolve(plsql, out_value)
