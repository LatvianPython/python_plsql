import pytest
from functools import reduce


def test_function_returns_value(plsql, simple_function):
    assert simple_function(21) == 42
    assert simple_function(p_int=21) == 42
    assert simple_function(None) is None
