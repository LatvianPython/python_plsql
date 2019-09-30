CREATE OR REPLACE FUNCTION function_blob(p_blob IN OUT BLOB)
RETURN BLOB IS
    v_blob BLOB;
BEGIN
    dbms_lob.createtemporary(v_blob, TRUE);
    FOR i IN 1 .. 1000 LOOP
        DBMS_LOB.APPEND(v_blob, p_blob);
    END LOOP;

    p_blob := v_blob;
    RETURN v_blob;
END function_blob;
