CREATE OR REPLACE PACKAGE BODY test_package AS

    PROCEDURE simple_procedure IS
    BEGIN
        NULL;
    END simple_procedure;

    FUNCTION simple_function(p_int IN INTEGER)
        RETURN INTEGER IS
    BEGIN
        RETURN p_int * p_int;
    END simple_function;

END test_package;

