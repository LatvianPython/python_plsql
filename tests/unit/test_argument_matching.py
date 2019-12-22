import pytest


def test_match_with_no_argument(plsql):
    assert plsql.simple_procedure._match()


def test_match_with_argument(plsql):
    procedure = plsql.with_argument

    assert procedure._match(1)
    assert procedure._match(p_int=1)
    assert not procedure._match()
    assert not procedure._match(1, 2)
    assert not procedure._match(p_int=1, p_str="2")
