import datetime


def test_simple_function(plsql):
    assert plsql.simple_function(p_int=5) == 5 + 5
    assert plsql.simple_function(p_int=None) is None


def test_simple_function_under_schema(plsql):
    assert plsql.test_user.simple_function(p_int=5) == 5 + 5


def test_function_with_defaults(plsql):
    assert plsql.function_with_defaults() == 5
    assert plsql.function_with_defaults(p_int_a=0) == 4
    assert plsql.function_with_defaults(p_int_b=0) == 1
    assert plsql.function_with_defaults(p_int_a=0, p_int_b=0) == 0


def test_string_function(plsql):
    assert plsql.string_function(p_str='test') == 'test' * 2


def test_function_in_out(plsql):
    result, in_out = plsql.function_in_out(p_int=21, p_float=1337.42, p_str='input')

    assert result == 42
    assert in_out['p_str'] == 'input: 42'
    assert in_out['p_float'] == 10.5


def test_datetime_func(plsql):
    date = datetime.datetime(year=2019, month=5, day=5)

    ten_days_ahead = date + datetime.timedelta(days=10)

    result, in_out = plsql.datetime_func(p_date=date)
    assert result == ten_days_ahead
    assert in_out['p_date'] == ten_days_ahead


def test_function_clob(plsql):
    clob = '1'
    result, in_out = plsql.function_clob(p_clob=clob)
    result, in_out['p_clob'] = result.read(), in_out['p_clob'].read()

    assert len(result) == len(in_out['p_clob']) == 10000
    assert type(clob) == type(result) == type(in_out['p_clob'])


def test_function_blob(plsql):
    blob = b'1'
    result, in_out = plsql.function_blob(p_blob=blob)
    result, in_out['p_blob'] = result.read(), in_out['p_blob'].read()

    assert len(result) == len(in_out['p_blob']) == 10000
    assert type(blob) == type(result) == type(in_out['p_blob'])
