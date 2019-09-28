def test_simple_function(plsql, simple_function):
    assert plsql.simple_function(p_int=5) == 5 + 5
    assert plsql.simple_function(p_int=None) is None


def test_function_with_defaults(plsql, function_with_defaults):
    assert plsql.function_with_defaults() == 5
    assert plsql.function_with_defaults(p_int_a=0) == 4
    assert plsql.function_with_defaults(p_int_b=0) == 1
    assert plsql.function_with_defaults(p_int_a=0, p_int_b=0) == 0


def test_string_function(plsql, string_function):
    assert plsql.string_function(p_str='test') == 'testtest'
