def test_basic_package_access(plsql):
    plsql.test_package.simple_procedure()


def test_basic_function(plsql):
    assert plsql.test_package.simple_function(p_int=10) == 100
