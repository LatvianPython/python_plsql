CREATE OR REPLACE PROCEDURE procedure_in_out_params(p_str IN OUT VARCHAR2) IS
    v_int INTEGER;
BEGIN
    v_int := TO_NUMBER(p_str) * 2;
    p_str := TO_CHAR(v_int);
END;