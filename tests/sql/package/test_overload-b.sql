CREATE OR REPLACE PACKAGE BODY test_overload AS

    FUNCTION simple_function(p_int IN INTEGER)
        RETURN INTEGER IS
    BEGIN
        RETURN p_int * p_int;
    END simple_function;

    FUNCTION simple_function(p_int IN INTEGER,
                             p_divide IN BOOLEAN)
        RETURN INTEGER IS
    BEGIN
        IF p_divide THEN
            RETURN p_int / p_int;
        ELSE
            RETURN p_int * p_int;
        END IF;

    END simple_function;

END test_overload;
