CREATE OR REPLACE PACKAGE test_in_out_params AS

    -- 0   placeholder for procedures with no arguments     -- ------||------
    -- 1   VARCHAR2, VARCHAR, STRING                        -- str
    PROCEDURE io_varchar2(p_param IN OUT VARCHAR2);

    PROCEDURE io_varchar(p_param IN OUT VARCHAR);

    PROCEDURE io_string(p_param IN OUT STRING);

    -- 2   NUMBER, INTEGER, SMALLINT, REAL, FLOAT, DECIMAL  -- float
    PROCEDURE io_number(p_param IN OUT NUMBER);

    PROCEDURE io_integer(p_param IN OUT INTEGER);

    PROCEDURE io_smallint(p_param IN OUT SMALLINT);

    PROCEDURE io_real(p_param IN OUT REAL);

    PROCEDURE io_float(p_param IN OUT FLOAT);

    PROCEDURE io_numeric(p_param IN OUT NUMERIC);

    PROCEDURE io_decimal(p_param IN OUT DECIMAL);

    -- 3   BINARY_INTEGER, PLS_INTEGER, POSITIVE, NATURAL   -- int
    PROCEDURE io_binary_integer(p_param IN OUT BINARY_INTEGER);

    PROCEDURE io_pls_integer(p_param IN OUT PLS_INTEGER);

    PROCEDURE io_positive(p_param IN OUT POSITIVE);

    PROCEDURE io_natural(p_param IN OUT NATURAL);

    -- 8   LONG ?CLOB?                                      -- str
    PROCEDURE io_clob(p_param IN OUT CLOB);

    PROCEDURE io_long(p_param IN OUT LONG);

    -- 11  ROWID                                            -- str
    PROCEDURE io_rowid(p_param IN OUT ROWID);

    -- 12  DATE                                             -- datetime.datetime
    PROCEDURE io_date(p_param IN OUT DATE);

    -- 23  RAW                                              -- bytes
    PROCEDURE io_raw(p_param IN OUT RAW);

    -- 24  LONG RAW                                         -- bytes
    PROCEDURE io_long_raw(p_param IN OUT LONG RAW);

    -- 58  OPAQUE TYPE                                      -- ??? XMLType IN OUT Oracle
    --PROCEDURE io_binary_integer(p_param IN OUT BINARY_INTEGER);

    -- 96  CHAR (ANSI FIXED CHAR), CHARACTER                -- str
    PROCEDURE io_char(p_param IN OUT CHAR);

    PROCEDURE io_character(p_param IN OUT CHARACTER);

    -- 106 MLSLABEL                                         -- ??? only backwards compatibility ???
    --PROCEDURE io_binary_integer(p_param IN OUT BINARY_INTEGER);

    -- 121 OBJECT                                           -- cx_Oracle.Object ???
    --PROCEDURE io_binary_integer(p_param IN OUT BINARY_INTEGER);

    -- 122 NESTED TABLE                                     -- list
    PROCEDURE io_nested(p_param IN OUT test_return.tt_nested);

    PROCEDURE io_nested_of_records(p_param IN OUT test_return.tt_nested_of_records);

    PROCEDURE io_nested_of_nested(p_param IN OUT test_return.tt_nested_of_nested);

    PROCEDURE io_nested_of_plsql_table(p_param IN OUT test_return.tt_nested_of_plsql_table);

    PROCEDURE io_nested_of_record_of_nested(p_param IN OUT test_return.tt_nested_of_record_of_nested);

    -- 123 VARRAY                                           -- list
    PROCEDURE io_varray(p_param IN OUT test_return.tt_varray);

    PROCEDURE io_varray_of_nested(p_param IN OUT test_return.tt_varray_of_nested);

    PROCEDURE io_varray_of_plsql_table(p_param IN OUT test_return.tt_varray_of_plsql_table);

    -- 178 TIME                                             -- datetime.datetime
    --PROCEDURE io_binary_integer(p_param IN OUT BINARY_INTEGER);

    -- 179 TIME WITH TIME ZONE                              -- datetime.datetime
    --PROCEDURE io_binary_integer(p_param IN OUT BINARY_INTEGER);

    -- 180 TIMESTAMP                                        -- datetime.datetime
    PROCEDURE io_timestamp(p_param IN OUT TIMESTAMP);

    -- 181 TIMESTAMP WITH TIME ZONE                         -- datetime.datetime
    --PROCEDURE io_binary_integer(p_param IN OUT BINARY_INTEGER);

    -- 231 TIMESTAMP WITH LOCAL TIME ZONE                   -- datetime.datetime
    --PROCEDURE io_binary_integer(p_param IN OUT BINARY_INTEGER);

    -- 250 PL/SQL RECORD                                    -- tuple - namedtuple
    PROCEDURE io_record(p_param IN OUT test_return.tr_record);

    PROCEDURE io_record_of_records(p_param IN OUT test_return.tr_record_of_records);

    PROCEDURE io_record_of_nested(p_param IN OUT test_return.tr_record_of_nested);

    PROCEDURE io_record_of_plsql_table(p_param IN OUT test_return.tr_record_of_plsql_table);

    -- 251 PL/SQL TABLE                                     -- mapping
    PROCEDURE io_plsql_table(p_param IN OUT test_return.tt_plsql_table);

    PROCEDURE io_plsql_table_of_records(p_param IN OUT test_return.tt_plsql_table_of_records);

    PROCEDURE io_plsql_table_of_nested(p_param IN OUT test_return.tt_plsql_table_of_nested);

    PROCEDURE io_plsql_table_of_plsql_table(p_param IN OUT test_return.tt_plsql_table_of_plsql_table);

    -- 252 PL/SQL BOOLEAN                                   -- bool
    PROCEDURE io_bool(p_param IN OUT BOOLEAN);


END test_in_out_params;
