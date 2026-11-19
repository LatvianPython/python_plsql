CREATE OR REPLACE PACKAGE BODY test_matching AS

    FUNCTION with_defaults(p_first  IN INTEGER,
                           p_second IN INTEGER DEFAULT 10,
                           p_third  IN INTEGER DEFAULT 100)
    RETURN INTEGER IS
    BEGIN
        RETURN p_first + p_second + p_third;
    END with_defaults;

    FUNCTION by_name(p_number IN INTEGER)
    RETURN VARCHAR2 IS
    BEGIN
        RETURN 'number';
    END by_name;

    FUNCTION by_name(p_text IN VARCHAR2)
    RETURN VARCHAR2 IS
    BEGIN
        RETURN 'text';
    END by_name;

END test_matching;
