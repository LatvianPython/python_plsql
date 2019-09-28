CREATE OR REPLACE FUNCTION function_in_out(p_int IN INTEGER,
                                           p_float OUT NUMBER,
                                           p_str IN OUT VARCHAR2)
    RETURN INTEGER IS
    v_int INTEGER;
BEGIN
    v_int := p_int * 2;
    p_float := p_int / 2;
    p_str := p_str || ': ' || TO_CHAR(p_int * 2);
    RETURN v_int;
END;