-- noinspection SqlDeprecateType

CREATE OR REPLACE PACKAGE BODY test_out_params AS

    -- 0   placeholder for procedures with no arguments     -- ------||------
    -- 1   VARCHAR2, VARCHAR, STRING                        -- str
    PROCEDURE out_varchar2(p_param OUT VARCHAR2) IS
    BEGIN
        p_param := test_return.ret_varchar2;
    END out_varchar2;

    PROCEDURE out_varchar(p_param OUT VARCHAR) IS
    BEGIN
        p_param := test_return.ret_varchar;
    END out_varchar;

    PROCEDURE out_string(p_param OUT STRING) IS
    BEGIN
        p_param := test_return.ret_string;
    END out_string;

    -- 2   NUMBER, INTEGER, SMALLINT, REAL, FLOAT, DECIMAL  -- float
    PROCEDURE out_number(p_param OUT NUMBER) IS
    BEGIN
        p_param := test_return.ret_number;
    END out_number;

    PROCEDURE out_integer(p_param OUT INTEGER) IS
    BEGIN
        p_param := test_return.ret_integer;
    END out_integer;

    PROCEDURE out_smallint(p_param OUT SMALLINT) IS
    BEGIN
        p_param := test_return.ret_smallint;
    END out_smallint;

    PROCEDURE out_real(p_param OUT REAL) IS
    BEGIN
        p_param := test_return.ret_real;
    END out_real;

    PROCEDURE out_float(p_param OUT FLOAT) IS
    BEGIN
        p_param := test_return.ret_float;
    END out_float;

    PROCEDURE out_numeric(p_param OUT NUMERIC) IS
    BEGIN
        p_param := test_return.ret_numeric;
    END out_numeric;

    PROCEDURE out_decimal(p_param OUT DECIMAL) IS
    BEGIN
        p_param := test_return.ret_decimal;
    END out_decimal;

    -- 3   BINARY_INTEGER, PLS_INTEGER, POSITIVE, NATURAL   -- int
    PROCEDURE out_binary_integer(p_param OUT BINARY_INTEGER) IS
    BEGIN
        p_param := test_return.ret_binary_integer;
    END;

    PROCEDURE out_pls_integer(p_param OUT PLS_INTEGER) IS
    BEGIN
        p_param := test_return.ret_pls_integer;
    END;

    PROCEDURE out_positive(p_param OUT POSITIVE) IS
    BEGIN
        p_param := test_return.ret_positive;
    END;

    PROCEDURE out_natural(p_param OUT NATURAL) IS
    BEGIN
        p_param := test_return.ret_natural;
    END;

    -- 8   LONG ?CLOB?                                      -- str
    PROCEDURE out_clob(p_param OUT CLOB) IS
    BEGIN
        p_param := test_return.ret_clob;
    END;

    PROCEDURE out_long(p_param OUT LONG) IS
    BEGIN
        p_param := test_return.ret_long;
    END;

    -- 11  ROWID                                            -- str
    PROCEDURE out_rowid(p_param OUT ROWID) IS
    BEGIN
        p_param := test_return.ret_rowid;
    END;

    -- 12  DATE                                             -- datetime.datetime
    PROCEDURE out_date(p_param OUT DATE) IS
    BEGIN
        p_param := test_return.ret_date;
    END;

    -- 23  RAW                                              -- bytes
    PROCEDURE out_raw(p_param OUT RAW) IS
    BEGIN
        p_param := test_return.ret_raw;
    END;

    -- 24  LONG RAW                                         -- bytes
    PROCEDURE out_long_raw(p_param OUT LONG RAW) IS
    BEGIN
        p_param := test_return.ret_long_raw;
    END;

    -- 58  OPAQUE TYPE                                      -- ??? XMLType OUT Oracle
    --PROCEDURE out_binary_integer(p_param OUT BINARY_INTEGER);

    -- 96  CHAR (ANSI FIXED CHAR), CHARACTER                -- str
    PROCEDURE out_char(p_param OUT CHAR) IS
    BEGIN
        p_param := test_return.ret_char;
    END;

    PROCEDURE out_character(p_param OUT CHARACTER) IS
    BEGIN
        p_param := test_return.ret_character;
    END;

    -- 106 MLSLABEL                                         -- ??? only backwards compatibility ???
    --PROCEDURE out_binary_integer(p_param OUT BINARY_INTEGER);

    -- 121 OBJECT                                           -- cx_Oracle.Object ???
    --PROCEDURE out_binary_integer(p_param OUT BINARY_INTEGER);

    -- 122 NESTED TABLE                                     -- list
    PROCEDURE out_nested(p_param OUT test_return.tt_nested) IS
    BEGIN
        p_param := test_return.ret_nested;
    END out_nested;

    PROCEDURE out_nested_of_records(p_param OUT test_return.tt_nested_of_records) IS
    BEGIN
        p_param := test_return.ret_nested_of_records;
    END out_nested_of_records;

    PROCEDURE out_nested_of_nested(p_param OUT test_return.tt_nested_of_nested) IS
    BEGIN
        p_param := test_return.ret_nested_of_nested;
    END out_nested_of_nested;

    PROCEDURE out_nested_of_plsql_table(p_param OUT test_return.tt_nested_of_plsql_table) IS
    BEGIN
        p_param := test_return.ret_nested_of_plsql_table;
    END out_nested_of_plsql_table;

    PROCEDURE out_nested_of_record_of_nested(p_param OUT test_return.tt_nested_of_record_of_nested) IS
    BEGIN
        p_param := test_return.ret_nested_of_record_of_nested;
    END out_nested_of_record_of_nested;

    -- 123 VARRAY                                           -- list
    PROCEDURE out_varray(p_param OUT test_return.tt_varray) IS
    BEGIN
        p_param := test_return.ret_varray;
    END out_varray;

    PROCEDURE out_varray_of_nested(p_param OUT test_return.tt_varray_of_nested) IS
    BEGIN
        p_param := test_return.ret_varray_of_nested;
    END out_varray_of_nested;

    PROCEDURE out_varray_of_plsql_table(p_param OUT test_return.tt_varray_of_plsql_table) IS
    BEGIN
        p_param := test_return.ret_varray_of_plsql_table;
    END out_varray_of_plsql_table;

    -- 178 TIME                                             -- datetime.datetime
    --PROCEDURE out_binary_integer(p_param OUT BINARY_INTEGER);

    -- 179 TIME WITH TIME ZONE                              -- datetime.datetime
    --PROCEDURE out_binary_integer(p_param OUT BINARY_INTEGER);

    -- 180 TIMESTAMP                                        -- datetime.datetime
    PROCEDURE out_timestamp(p_param OUT TIMESTAMP) IS
    BEGIN
        p_param := test_return.ret_timestamp;
    END out_timestamp;

    -- 181 TIMESTAMP WITH TIME ZONE                         -- datetime.datetime
    --PROCEDURE out_binary_integer(p_param OUT BINARY_INTEGER);

    -- 231 TIMESTAMP WITH LOCAL TIME ZONE                   -- datetime.datetime
    --PROCEDURE out_binary_integer(p_param OUT BINARY_INTEGER);

    -- 250 PL/SQL RECORD                                    -- tuple - namedtuple
    PROCEDURE out_record(p_param OUT test_return.tr_record) IS
    BEGIN
        p_param := test_return.ret_record;
    END;

    PROCEDURE out_record_of_records(p_param OUT test_return.tr_record_of_records) IS
    BEGIN
        p_param := test_return.ret_record_of_records;
    END out_record_of_records;

    PROCEDURE out_record_of_nested(p_param OUT test_return.tr_record_of_nested) IS
    BEGIN
        p_param := test_return.ret_record_of_nested;
    END out_record_of_nested;

    PROCEDURE out_record_of_plsql_table(p_param OUT test_return.tr_record_of_plsql_table) IS
    BEGIN
        p_param := test_return.ret_record_of_plsql_table;
    END out_record_of_plsql_table;

    -- 251 PL/SQL TABLE                                     -- mapping
    PROCEDURE out_plsql_table(p_param OUT test_return.tt_plsql_table) IS
    BEGIN
        p_param := test_return.ret_plsql_table;
    END out_plsql_table;

    PROCEDURE out_plsql_table_of_records(p_param OUT test_return.tt_plsql_table_of_records) IS
    BEGIN
        p_param := test_return.ret_plsql_table_of_records;
    END out_plsql_table_of_records;

    PROCEDURE out_plsql_table_of_nested(p_param OUT test_return.tt_plsql_table_of_nested) IS
    BEGIN
        p_param := test_return.ret_plsql_table_of_nested;
    END out_plsql_table_of_nested;

    PROCEDURE out_plsql_table_of_plsql_table(p_param OUT test_return.tt_plsql_table_of_plsql_table) IS
    BEGIN
        p_param := test_return.ret_plsql_table_of_plsql_table;
    END out_plsql_table_of_plsql_table;

    -- 252 PL/SQL BOOLEAN                                   -- bool
    PROCEDURE out_bool(p_param OUT BOOLEAN) IS
    BEGIN
        p_param := test_return.ret_bool;
    END;

END test_out_params;
