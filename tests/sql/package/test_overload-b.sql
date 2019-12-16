CREATE OR REPLACE PACKAGE BODY test_overload AS

    FUNCTION to_string(p_in IN VARCHAR2)
    RETURN VARCHAR2 IS
    BEGIN
        RETURN p_in;
    END to_string;

    FUNCTION to_string(p_in IN INTEGER)
    RETURN VARCHAR2 IS
    BEGIN
        RETURN TO_CHAR(p_in);
    END to_string;

END test_overload;
