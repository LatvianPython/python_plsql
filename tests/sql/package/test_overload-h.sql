CREATE OR REPLACE PACKAGE test_overload AS

    FUNCTION simple_function(p_int IN INTEGER,
                             p_divide IN BOOLEAN)
        RETURN INTEGER;

    FUNCTION simple_function(p_int IN INTEGER)
        RETURN INTEGER;

END test_overload;
