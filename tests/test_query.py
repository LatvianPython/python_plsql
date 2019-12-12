import pytest


def test_with_no_binds(plsql):
    plsql.query("""SELECT 1 FROM dual""").first == 1
