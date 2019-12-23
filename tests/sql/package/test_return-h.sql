CREATE OR REPLACE PACKAGE test_return AS
    -- 0   placeholder for procedures with no arguments     -- ------||------
    -- 1   VARCHAR2, VARCHAR, STRING                        -- str
    FUNCTION ret_varchar
    RETURN VARCHAR2;

    -- 2   NUMBER, INTEGER, SMALLINT, REAL, FLOAT, DECIMAL  -- float
    FUNCTION ret_number
    RETURN NUMBER;

    -- 3   BINARY_INTEGER, PLS_INTEGER, POSITIVE, NATURAL   -- int
    FUNCTION ret_binary_integer
    RETURN BINARY_INTEGER;

    -- 8   LONG ?CLOB?                                      -- str
    FUNCTION ret_clob
    RETURN CLOB;

    -- 11  ROWID                                            -- str
    FUNCTION ret_rowid
    RETURN ROWID;

    -- 12  DATE                                             -- datetime.datetime
    FUNCTION ret_date
    RETURN DATE;

    -- 23  RAW                                              -- bytes
    FUNCTION ret_raw
    RETURN RAW;

    -- 24  LONG RAW                                         -- bytes
    FUNCTION ret_long_raw
    RETURN LONG RAW;

    -- 58  OPAQUE TYPE                                      -- ??? XMLType in Oracle
    --FUNCTION ret_binary_integer
    --RETURN BINARY_INTEGER;

    -- 96  CHAR (ANSI FIXED CHAR), CHARACTER                -- str
    FUNCTION ret_char
    RETURN CHAR;

    -- 106 MLSLABEL                                         -- ??? only backwards compatibility ???
    --FUNCTION ret_binary_integer
    --RETURN BINARY_INTEGER;

    -- 121 OBJECT                                           -- cx_Oracle.Object ???
    --FUNCTION ret_binary_integer
    --RETURN BINARY_INTEGER;

    -- 122 NESTED TABLE                                     -- list
    --FUNCTION ret_binary_integer
    --RETURN BINARY_INTEGER;

    -- 123 VARRAY                                           -- list
    --FUNCTION ret_binary_integer
    --RETURN BINARY_INTEGER;

    -- 178 TIME                                             -- datetime.datetime
    --FUNCTION ret_binary_integer
    --RETURN BINARY_INTEGER;

    -- 179 TIME WITH TIME ZONE                              -- datetime.datetime
    --FUNCTION ret_binary_integer
    --RETURN BINARY_INTEGER;

    -- 180 TIMESTAMP                                        -- datetime.datetime
    --FUNCTION ret_binary_integer
    --RETURN BINARY_INTEGER;

    -- 181 TIMESTAMP WITH TIME ZONE                         -- datetime.datetime
    --FUNCTION ret_binary_integer
    --RETURN BINARY_INTEGER;

    -- 231 TIMESTAMP WITH LOCAL TIME ZONE                   -- datetime.datetime
    --FUNCTION ret_binary_integer
    --RETURN BINARY_INTEGER;

    -- 250 PL/SQL RECORD                                    -- tuple - namedtuple
    --FUNCTION ret_binary_integer
    --RETURN BINARY_INTEGER;

    -- 251 PL/SQL TABLE                                     -- mapping
    --FUNCTION ret_binary_integer
    --RETURN BINARY_INTEGER;

    -- 252 PL/SQL BOOLEAN                                   -- bool
    FUNCTION ret_bool
    RETURN BOOLEAN;


END test_return;
