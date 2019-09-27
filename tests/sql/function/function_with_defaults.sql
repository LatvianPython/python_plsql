CREATE OR REPLACE FUNCTION function_with_defaults(p_int_a IN INTEGER DEFAULT 1,
                                                  p_int_b IN INTEGER DEFAULT 4)
RETURN INTEGER IS
BEGIN
    RETURN p_int_a + p_int_b;
END function_with_defaults;
