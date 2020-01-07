CREATE OR REPLACE PROCEDURE simple_procedure IS
    v_int INTEGER DEFAULT 42;
BEGIN
    raise_application_error(-20001, 'You called me ' || TO_CHAR(v_int));
END;