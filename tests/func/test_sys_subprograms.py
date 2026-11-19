import pytest


@pytest.mark.xfail(reason="SYS.DATABASE_NAME has no argument metadata to describe")
def test_database_name(plsql):
    assert plsql.sys.database_name() == "orcl"
