CREATE OR REPLACE PACKAGE test_package AS
    PROCEDURE simple_procedure;

    FUNCTION simple_function(p_int IN INTEGER)
        RETURN INTEGER;
END test_package;
