CREATE OR REPLACE PACKAGE test_matching AS

    FUNCTION with_defaults(p_first  IN INTEGER,
                           p_second IN INTEGER DEFAULT 10,
                           p_third  IN INTEGER DEFAULT 100)
    RETURN INTEGER;

    FUNCTION by_name(p_number IN INTEGER)
    RETURN VARCHAR2;

    FUNCTION by_name(p_text IN VARCHAR2)
    RETURN VARCHAR2;

END test_matching;
