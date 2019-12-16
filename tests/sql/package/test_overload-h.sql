CREATE OR REPLACE PACKAGE test_overload AS

    FUNCTION to_string(p_in IN VARCHAR2)
    RETURN VARCHAR2;

    FUNCTION to_string(p_in IN INTEGER)
    RETURN VARCHAR2;

END test_overload;
