CREATE OR REPLACE PACKAGE BODY test_package AS

    PROCEDURE simple_procedure IS
    BEGIN
        NULL;
    END simple_procedure;

    FUNCTION simple_function
    RETURN INTEGER IS
    BEGIN
        RETURN 1;
    END simple_function;

END test_package;
