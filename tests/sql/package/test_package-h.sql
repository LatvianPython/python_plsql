CREATE OR REPLACE PACKAGE test_package AS

    PROCEDURE simple_procedure;

    PROCEDURE proc_with_params(p_varchar IN VARCHAR2);

    FUNCTION simple_function(p_int IN INTEGER)
    RETURN INTEGER;

END test_package;
