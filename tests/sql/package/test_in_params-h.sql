CREATE OR REPLACE PACKAGE test_in_params AS

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

    TYPE tt_varray IS VARRAY(10) OF PLS_INTEGER;

    TYPE tt_varray_of_nested IS VARRAY(10) OF tt_nested;

    TYPE tt_varray_of_plsql_table IS VARRAY(10) OF tt_plsql_table;

    -- 0   placeholder for procedures with no arguments     -- ------||------
    -- 1   VARCHAR2, VARCHAR, STRING                        -- str
    PROCEDURE in_varchar2(p_param IN VARCHAR2);

    PROCEDURE in_varchar(p_param IN VARCHAR);

    PROCEDURE in_string(p_param IN STRING);

    -- 2   NUMBER, INTEGER, SMALLINT, REAL, FLOAT, DECIMAL  -- float
    PROCEDURE in_number(p_param IN NUMBER);

    PROCEDURE in_integer(p_param IN INTEGER);

    PROCEDURE in_smallint(p_param IN SMALLINT);

    PROCEDURE in_real(p_param IN REAL);

    PROCEDURE in_float(p_param IN FLOAT);

    PROCEDURE in_numeric(p_param IN NUMERIC);

    PROCEDURE in_decimal(p_param IN DECIMAL);

    -- 3   BINARY_INTEGER, PLS_INTEGER, POSITIVE, NATURAL   -- int
    PROCEDURE in_binary_integer(p_param IN BINARY_INTEGER);

    PROCEDURE in_pls_integer(p_param IN PLS_INTEGER);

    PROCEDURE in_positive(p_param IN POSITIVE);

    PROCEDURE in_natural(p_param IN NATURAL);

    -- 8   LONG ?CLOB?                                      -- str
    PROCEDURE in_clob(p_param IN CLOB);

    PROCEDURE in_long(p_param IN LONG);

    -- 11  ROWID                                            -- str
    PROCEDURE in_rowid(p_param IN ROWID);

    -- 12  DATE                                             -- datetime.datetime
    PROCEDURE in_date(p_param IN DATE);

    -- 23  RAW                                              -- bytes
    PROCEDURE in_raw(p_param IN RAW);

    -- 24  LONG RAW                                         -- bytes
    PROCEDURE in_long_raw(p_param IN LONG RAW);

    -- 58  OPAQUE TYPE                                      -- ??? XMLType in Oracle
    --PROCEDURE in_binary_integer(p_param IN BINARY_INTEGER);

    -- 96  CHAR (ANSI FIXED CHAR), CHARACTER                -- str
    PROCEDURE in_char(p_param IN CHAR);

    PROCEDURE in_character(p_param IN CHARACTER);

    -- 106 MLSLABEL                                         -- ??? only backwards compatibility ???
    --PROCEDURE in_binary_integer(p_param IN BINARY_INTEGER);

    -- 121 OBJECT                                           -- cx_Oracle.Object ???
    --PROCEDURE in_binary_integer(p_param IN BINARY_INTEGER);

    -- 122 NESTED TABLE                                     -- list
    PROCEDURE in_nested(p_param IN tt_nested);

    PROCEDURE in_nested_of_records(p_param IN tt_nested_of_records);

    PROCEDURE in_nested_of_nested(p_param IN tt_nested_of_nested);

    PROCEDURE in_nested_of_plsql_table(p_param IN tt_nested_of_plsql_table);

    PROCEDURE in_nested_of_record_of_nested(p_param IN tt_nested_of_record_of_nested);

    -- 123 VARRAY                                           -- list
    PROCEDURE in_varray(p_param IN tt_varray);

    PROCEDURE in_varray_of_nested(p_param IN tt_varray_of_nested);

    PROCEDURE in_varray_of_plsql_table(p_param IN tt_varray_of_plsql_table);

    -- 178 TIME                                             -- datetime.datetime
    --PROCEDURE in_binary_integer(p_param IN BINARY_INTEGER);

    -- 179 TIME WITH TIME ZONE                              -- datetime.datetime
    --PROCEDURE in_binary_integer(p_param IN BINARY_INTEGER);

    -- 180 TIMESTAMP                                        -- datetime.datetime
    PROCEDURE in_timestamp(p_param IN TIMESTAMP);

    -- 181 TIMESTAMP WITH TIME ZONE                         -- datetime.datetime
    --PROCEDURE in_binary_integer(p_param IN BINARY_INTEGER);

    -- 231 TIMESTAMP WITH LOCAL TIME ZONE                   -- datetime.datetime
    --PROCEDURE in_binary_integer(p_param IN BINARY_INTEGER);

    -- 250 PL/SQL RECORD                                    -- tuple - namedtuple
    PROCEDURE in_record(p_param IN tr_record);

    PROCEDURE in_record_of_records(p_param IN tr_record_of_records);

    PROCEDURE in_record_of_nested(p_param IN tr_record_of_nested);

    PROCEDURE in_record_of_plsql_table(p_param IN tr_record_of_plsql_table);

    -- 251 PL/SQL TABLE                                     -- mapping
    PROCEDURE in_plsql_table(p_param IN tt_plsql_table);

    PROCEDURE in_plsql_table_of_records(p_param IN tt_plsql_table_of_records);

    PROCEDURE in_plsql_table_of_nested(p_param IN tt_plsql_table_of_nested);

    PROCEDURE in_plsql_table_of_plsql_table(p_param IN tt_plsql_table_of_plsql_table);

    -- 252 PL/SQL BOOLEAN                                   -- bool
    PROCEDURE in_bool(p_param IN BOOLEAN);


END test_in_params;
