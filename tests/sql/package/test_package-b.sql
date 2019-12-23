CREATE OR REPLACE PACKAGE BODY test_package AS

    PROCEDURE simple_procedure IS
        v_int INTEGER DEFAULT 42;
    BEGIN
        raise_application_error(-20001, 'You called me ' || TO_CHAR(v_int));
    END simple_procedure;

    PROCEDURE proc_with_params(p_varchar IN VARCHAR2) IS
    BEGIN
        raise_application_error(-20002, 'p_varchar=' || NVL(p_varchar, 'NULL'));
    END;

    FUNCTION simple_function(p_int IN INTEGER)
    RETURN INTEGER IS
    BEGIN
        RETURN p_int * 2;
    END simple_function;

END test_package;
