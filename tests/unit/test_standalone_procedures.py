import pytest


@pytest.fixture(scope="module", params=["simple_procedure", "synonym_procedure"])
def procedure(plsql, request):
    return getattr(plsql, request.param)


def test_procedure_is_found(procedure):
    assert procedure.resolved.name == "SIMPLE_PROCEDURE"


def test_standalone_procedures_are_not_overloaded(procedure):
    assert not procedure.is_overloaded


def test_standalone_procedures_are_standalone(procedure):
    assert procedure.standalone


def test_procedure_identified_as_such(procedure):
    assert procedure.is_procedure
    assert not procedure.is_function
