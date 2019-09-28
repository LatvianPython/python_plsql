CREATE OR REPLACE PROCEDURE procedure_out_params(p_str OUT VARCHAR2) IS
    v_int INTEGER;
BEGIN
    v_int := 21 * 2;
    p_str := TO_CHAR(v_int);
END;