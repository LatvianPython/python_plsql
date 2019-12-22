from python_plsql import DatabaseError, NotFound
import pytest


def test_procedure_gets_called(simple_procedure):
    """Checking if database executes the procedure, which is set to raise an application error"""
    with pytest.raises(DatabaseError, match="ORA-20001.+You called me.+42"):
        simple_procedure()
