CREATE OR REPLACE FUNCTION function_clob(p_clob IN OUT CLOB)
RETURN CLOB IS
    v_clob CLOB;
BEGIN
    FOR i IN 1 .. 10000 LOOP
        v_clob := v_clob || p_clob;
    END LOOP;

    p_clob := v_clob;
    RETURN v_clob;
END function_clob;
