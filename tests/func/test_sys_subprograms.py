import pytest


@pytest.mark.xfail(msg="does not work")
def test_database_name(plsql):
    assert plsql.sys.database_name() == "orcl"
