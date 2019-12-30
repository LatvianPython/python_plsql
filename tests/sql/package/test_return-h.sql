CREATE OR REPLACE PACKAGE test_return AS

    TYPE tr_record IS RECORD (
        t_int_1 PLS_INTEGER,
        t_int_2 PLS_INTEGER,
        t_int_3 PLS_INTEGER
    );

    TYPE tr_record_of_records IS RECORD (
        t_int_1 PLS_INTEGER,
        t_rec_2 tr_record,
        t_rec_3 tr_record
    );

    TYPE tt_nested IS TABLE OF PLS_INTEGER;

    TYPE tr_record_of_nested IS RECORD (
        t_int_1 PLS_INTEGER,
        t_nes_2 tt_nested,
        t_nes_3 tt_nested
    );

    TYPE tt_nested_of_records IS TABLE OF tr_record;

    TYPE tt_nested_of_nested IS TABLE OF tt_nested;

    TYPE tt_plsql_table IS TABLE OF PLS_INTEGER INDEX BY PLS_INTEGER;

    TYPE tr_record_of_plsql_table IS RECORD (
        t_int_1 PLS_INTEGER,
        t_pls_2 tt_plsql_table,
        t_pls_3 tt_plsql_table
    );

    TYPE tt_nested_of_record_of_nested IS TABLE OF tr_record_of_nested;

    TYPE tt_plsql_table_of_plsql_table IS TABLE OF tt_plsql_table INDEX BY PLS_INTEGER;

    TYPE tt_plsql_table_of_nested IS TABLE OF tt_nested INDEX BY PLS_INTEGER;

    TYPE tt_plsql_table_of_records IS TABLE OF tr_record INDEX BY PLS_INTEGER;

    TYPE tt_nested_of_plsql_table IS TABLE OF tt_plsql_table;

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
    FUNCTION ret_nested
    RETURN tt_nested;

    FUNCTION ret_nested_of_records
    RETURN tt_nested_of_records;

    FUNCTION ret_nested_of_nested
    RETURN tt_nested_of_nested;

    FUNCTION ret_nested_of_plsql_table
    RETURN tt_nested_of_plsql_table;

    FUNCTION ret_nested_of_record_of_nested
    RETURN tt_nested_of_record_of_nested;

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
    FUNCTION ret_record
    RETURN tr_record;

    FUNCTION ret_record_of_records
    RETURN tr_record_of_records;

    FUNCTION ret_record_of_nested
    RETURN tr_record_of_nested;

    FUNCTION ret_record_of_plsql_table
    RETURN tr_record_of_plsql_table;

    -- 251 PL/SQL TABLE                                     -- mapping
    FUNCTION ret_plsql_table
    RETURN tt_plsql_table;

    FUNCTION ret_plsql_table_of_records
    RETURN tt_plsql_table_of_records;

    FUNCTION ret_plsql_table_of_nested
    RETURN tt_plsql_table_of_nested;

    FUNCTION ret_plsql_table_of_plsql_table
    RETURN tt_plsql_table_of_plsql_table;

    -- 252 PL/SQL BOOLEAN                                   -- bool
    FUNCTION ret_bool
    RETURN BOOLEAN;


END test_return;
