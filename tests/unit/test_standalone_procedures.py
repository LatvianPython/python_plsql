import pytest


def test_procedure_found_in_same_schema(plsql):
    procedure = plsql.simple_procedure
    assert procedure.resolved.name == "SIMPLE_PROCEDURE"


def test_procedure_found_with_synonym(plsql):
    procedure = plsql.test_synonym_procedure
    assert procedure.resolved.name == "SIMPLE_PROCEDURE"


@pytest.fixture(scope="module", params=["simple_procedure", "test_synonym_procedure"])
def procedure(plsql, request):
    return getattr(plsql, request.param)


def test_standalone_procedures_are_not_overloaded(plsql, procedure):
    assert not procedure.overloaded


def test_standalone_procedures_are_standalone(plsql, procedure):
    assert procedure.standalone
