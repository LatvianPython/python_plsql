def test_simple_procedure(plsql, simple_procedure):
    plsql.simple_procedure()


def test_procedure_out_params(plsql, procedure_out_params):
    result = plsql.procedure_out_params()
    assert result == {'p_str': '42'}


def test_procedure_in_out_params(plsql, procedure_in_out_params):
    result = plsql.procedure_in_out_params(p_str='21')
    assert result == {'p_str': '42'}
