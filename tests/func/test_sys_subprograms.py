def test_database_name(plsql):
    assert plsql.sys.database_name() == "orcl"
