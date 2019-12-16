import pytest


def test_procedure_found(plsql):
    procedure = plsql.simple_procedure
    assert procedure.resolved.name == "SIMPLE_PROCEDURE"
