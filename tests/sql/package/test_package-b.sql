CREATE OR REPLACE PACKAGE BODY test_package AS

    PROCEDURE simple_procedure IS
        v_int INTEGER DEFAULT 42;
    BEGIN
        raise_application_error(-20001, 'You called me :) ' || TO_CHAR(v_int));
    END simple_procedure;

    FUNCTION simple_function
    RETURN INTEGER IS
    BEGIN
        RETURN 1;
    END simple_function;

END test_package;
