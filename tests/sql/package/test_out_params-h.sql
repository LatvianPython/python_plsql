CREATE OR REPLACE PACKAGE test_out_params AS

    -- 0   placeholder for procedures with no arguments     -- ------||------
    -- 1   VARCHAR2, VARCHAR, STRING                        -- str
    PROCEDURE out_varchar2(p_param OUT VARCHAR2);

    PROCEDURE out_varchar(p_param OUT VARCHAR);

    PROCEDURE out_string(p_param OUT STRING);

    -- 2   NUMBER, INTEGER, SMALLINT, REAL, FLOAT, DECIMAL  -- float
    PROCEDURE out_number(p_param OUT NUMBER);

    PROCEDURE out_integer(p_param OUT INTEGER);

    PROCEDURE out_smallint(p_param OUT SMALLINT);

    PROCEDURE out_real(p_param OUT REAL);

    PROCEDURE out_float(p_param OUT FLOAT);

    PROCEDURE out_numeric(p_param OUT NUMERIC);

    PROCEDURE out_decimal(p_param OUT DECIMAL);

    -- 3   BINARY_INTEGER, PLS_INTEGER, POSITIVE, NATURAL   -- int
    PROCEDURE out_binary_integer(p_param OUT BINARY_INTEGER);

    PROCEDURE out_pls_integer(p_param OUT PLS_INTEGER);

    PROCEDURE out_positive(p_param OUT POSITIVE);

    PROCEDURE out_natural(p_param OUT NATURAL);

    -- 8   LONG ?CLOB?                                      -- str
    PROCEDURE out_clob(p_param OUT CLOB);

    PROCEDURE out_long(p_param OUT LONG);

    -- 11  ROWID                                            -- str
    PROCEDURE out_rowid(p_param OUT ROWID);

    -- 12  DATE                                             -- datetime.datetime
    PROCEDURE out_date(p_param OUT DATE);

    -- 23  RAW                                              -- bytes
    PROCEDURE out_raw(p_param OUT RAW);

    -- 24  LONG RAW                                         -- bytes
    PROCEDURE out_long_raw(p_param OUT LONG RAW);

    -- 58  OPAQUE TYPE                                      -- ??? XMLType OUT Oracle
    --PROCEDURE out_binary_integer(p_param OUT BINARY_INTEGER);

    -- 96  CHAR (ANSI FIXED CHAR), CHARACTER                -- str
    PROCEDURE out_char(p_param OUT CHAR);

    PROCEDURE out_character(p_param OUT CHARACTER);

    -- 106 MLSLABEL                                         -- ??? only backwards compatibility ???
    --PROCEDURE out_binary_integer(p_param OUT BINARY_INTEGER);

    -- 121 OBJECT                                           -- cx_Oracle.Object ???
    --PROCEDURE out_binary_integer(p_param OUT BINARY_INTEGER);

    -- 122 NESTED TABLE                                     -- list
    PROCEDURE out_nested(p_param OUT test_return.tt_nested);

    PROCEDURE out_nested_of_records(p_param OUT test_return.tt_nested_of_records);

    PROCEDURE out_nested_of_nested(p_param OUT test_return.tt_nested_of_nested);

    PROCEDURE out_nested_of_plsql_table(p_param OUT test_return.tt_nested_of_plsql_table);

    PROCEDURE out_nested_of_record_of_nested(p_param OUT test_return.tt_nested_of_record_of_nested);

    -- 123 VARRAY                                           -- list
    PROCEDURE out_varray(p_param OUT test_return.tt_varray);

    PROCEDURE out_varray_of_nested(p_param OUT test_return.tt_varray_of_nested);

    PROCEDURE out_varray_of_plsql_table(p_param OUT test_return.tt_varray_of_plsql_table);

    -- 178 TIME                                             -- datetime.datetime
    --PROCEDURE out_binary_integer(p_param OUT BINARY_INTEGER);

    -- 179 TIME WITH TIME ZONE                              -- datetime.datetime
    --PROCEDURE out_binary_integer(p_param OUT BINARY_INTEGER);

    -- 180 TIMESTAMP                                        -- datetime.datetime
    PROCEDURE out_timestamp(p_param OUT TIMESTAMP);

    -- 181 TIMESTAMP WITH TIME ZONE                         -- datetime.datetime
    --PROCEDURE out_binary_integer(p_param OUT BINARY_INTEGER);

    -- 231 TIMESTAMP WITH LOCAL TIME ZONE                   -- datetime.datetime
    --PROCEDURE out_binary_integer(p_param OUT BINARY_INTEGER);

    -- 250 PL/SQL RECORD                                    -- tuple - namedtuple
    PROCEDURE out_record(p_param OUT test_return.tr_record);

    PROCEDURE out_record_of_records(p_param OUT test_return.tr_record_of_records);

    PROCEDURE out_record_of_nested(p_param OUT test_return.tr_record_of_nested);

    PROCEDURE out_record_of_plsql_table(p_param OUT test_return.tr_record_of_plsql_table);

    -- 251 PL/SQL TABLE                                     -- mapping
    PROCEDURE out_plsql_table(p_param OUT test_return.tt_plsql_table);

    PROCEDURE out_plsql_table_of_records(p_param OUT test_return.tt_plsql_table_of_records);

    PROCEDURE out_plsql_table_of_nested(p_param OUT test_return.tt_plsql_table_of_nested);

    PROCEDURE out_plsql_table_of_plsql_table(p_param OUT test_return.tt_plsql_table_of_plsql_table);

    -- 252 PL/SQL BOOLEAN                                   -- bool
    PROCEDURE out_bool(p_param OUT BOOLEAN);


END test_out_params;
