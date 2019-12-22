import pytest


def test_single_column_returns_just_the_value(plsql):
    assert plsql.query("""SELECT 1    FROM dual""").first == 1
    assert plsql.query("""SELECT 'a'  FROM dual""").first == "a"
    assert plsql.query("""SELECT 3.5  FROM dual""").first == 3.5
    assert plsql.query("""SELECT NULL FROM dual""").first is None


def test_select_with_multiple_columns_returns_named_tuples(plsql):
    result = plsql.query("""SELECT 1 AS first, 2 AS second FROM dual""").first
    assert (result.first, result.second) == (1, 2)


def test_can_iterate_over_multiple_rows(plsql):
    assert sum(plsql.query("""SELECT level FROM dual CONNECT BY level < 10""")) == 45


def test_can_use_positional_binds(plsql):
    bind_value = 6
    assert plsql.query("""SELECT :a FROM dual""", bind_value).first == bind_value


def test_can_use_binds_by_name(plsql):
    bind_value = 6
    assert plsql.query("""SELECT :b FROM dual""", b=bind_value).first == bind_value


def test_binding_by_position_and_name_raises_an_exception(plsql):
    with pytest.raises(ValueError, match="Can not bind both by position and name"):
        plsql.query("""SELECT :c, :d FROM dual""", 5, d=5)
