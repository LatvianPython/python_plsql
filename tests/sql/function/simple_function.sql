CREATE OR REPLACE FUNCTION simple_function(p_int IN INTEGER)
RETURN INTEGER IS
BEGIN
    RETURN p_int * 2;
END simple_function;
