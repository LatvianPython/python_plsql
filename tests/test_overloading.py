def test_simple_overloading(plsql):
    assert plsql.test_overload.simple_function(p_int=5) == 5 ** 2
    assert plsql.test_overload.simple_function(p_int=5, p_divide=True) == 5 ** 0
