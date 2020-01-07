-- noinspection SqlDeprecateType

CREATE OR REPLACE PACKAGE BODY test_in_out_params AS

    -- 0   placeholder for procedures with no arguments     -- ------||------
    -- 1   VARCHAR2, VARCHAR, STRING                        -- str
    PROCEDURE io_varchar2(p_param IN OUT VARCHAR2) IS
    BEGIN
        test_in_params.in_varchar2(p_param => p_param);
    END io_varchar2;

    PROCEDURE io_varchar(p_param IN OUT VARCHAR) IS
    BEGIN
        test_in_params.in_varchar(p_param => p_param);
    END io_varchar;

    PROCEDURE io_string(p_param IN OUT STRING) IS
    BEGIN
        test_in_params.in_string(p_param => p_param);
    END io_string;

    -- 2   NUMBER, INTEGER, SMALLINT, REAL, FLOAT, DECIMAL  -- float
    PROCEDURE io_number(p_param IN OUT NUMBER) IS
    BEGIN
        test_in_params.in_number(p_param => p_param);
    END io_number;

    PROCEDURE io_integer(p_param IN OUT INTEGER) IS
    BEGIN
        test_in_params.in_integer(p_param => p_param);
    END io_integer;

    PROCEDURE io_smallint(p_param IN OUT SMALLINT) IS
    BEGIN
        test_in_params.in_smallint(p_param => p_param);
    END io_smallint;

    PROCEDURE io_real(p_param IN OUT REAL) IS
    BEGIN
        test_in_params.in_real(p_param => p_param);
    END io_real;

    PROCEDURE io_float(p_param IN OUT FLOAT) IS
    BEGIN
        test_in_params.in_float(p_param => p_param);
    END io_float;

    PROCEDURE io_numeric(p_param IN OUT NUMERIC) IS
    BEGIN
        test_in_params.in_numeric(p_param => p_param);
    END io_numeric;

    PROCEDURE io_decimal(p_param IN OUT DECIMAL) IS
    BEGIN
        test_in_params.in_decimal(p_param => p_param);
    END io_decimal;

    -- 3   BINARY_INTEGER, PLS_INTEGER, POSITIVE, NATURAL   -- int
    PROCEDURE io_binary_integer(p_param IN OUT BINARY_INTEGER) IS
    BEGIN
        test_in_params.in_binary_integer(p_param => p_param);
    END;

    PROCEDURE io_pls_integer(p_param IN OUT PLS_INTEGER) IS
    BEGIN
        test_in_params.in_pls_integer(p_param => p_param);
    END;

    PROCEDURE io_positive(p_param IN OUT POSITIVE) IS
    BEGIN
        test_in_params.in_positive(p_param => p_param);
    END;

    PROCEDURE io_natural(p_param IN OUT NATURAL) IS
    BEGIN
        test_in_params.in_natural(p_param => p_param);
    END;

    -- 8   LONG ?CLOB?                                      -- str
    PROCEDURE io_clob(p_param IN OUT CLOB) IS
    BEGIN
        test_in_params.in_clob(p_param => p_param);
    END;

    PROCEDURE io_long(p_param IN OUT LONG) IS
    BEGIN
        test_in_params.in_long(p_param => p_param);
    END;

    -- 11  ROWID                                            -- str
    PROCEDURE io_rowid(p_param IN OUT ROWID) IS
    BEGIN
        test_in_params.in_rowid(p_param => p_param);
    END;

    -- 12  DATE                                             -- datetime.datetime
    PROCEDURE io_date(p_param IN OUT DATE) IS
    BEGIN
        test_in_params.in_date(p_param => p_param);
    END;

    -- 23  RAW                                              -- bytes
    PROCEDURE io_raw(p_param IN OUT RAW) IS
    BEGIN
        test_in_params.in_raw(p_param => p_param);
    END;

    -- 24  LONG RAW                                         -- bytes
    PROCEDURE io_long_raw(p_param IN OUT LONG RAW) IS
    BEGIN
        test_in_params.in_long_raw(p_param => p_param);
    END;

    -- 58  OPAQUE TYPE                                      -- ??? XMLType IN OUT Oracle
    --PROCEDURE io_binary_integer(p_param IN OUT BINARY_INTEGER);

    -- 96  CHAR (ANSI FIXED CHAR), CHARACTER                -- str
    PROCEDURE io_char(p_param IN OUT CHAR) IS
    BEGIN
        test_in_params.in_char(p_param => p_param);
    END;

    PROCEDURE io_character(p_param IN OUT CHARACTER) IS
    BEGIN
        test_in_params.in_character(p_param => p_param);
    END;

    -- 106 MLSLABEL                                         -- ??? only backwards compatibility ???
    --PROCEDURE io_binary_integer(p_param IN OUT BINARY_INTEGER);

    -- 121 OBJECT                                           -- cx_Oracle.Object ???
    --PROCEDURE io_binary_integer(p_param IN OUT BINARY_INTEGER);

    -- 122 NESTED TABLE                                     -- list
    PROCEDURE io_nested(p_param IN OUT test_return.tt_nested) IS
    BEGIN
        test_in_params.in_nested(p_param => p_param);
    END io_nested;

    PROCEDURE io_nested_of_records(p_param IN OUT test_return.tt_nested_of_records) IS
    BEGIN
        test_in_params.in_nested_of_records(p_param => p_param);
    END io_nested_of_records;

    PROCEDURE io_nested_of_nested(p_param IN OUT test_return.tt_nested_of_nested) IS
    BEGIN
        test_in_params.in_nested_of_nested(p_param => p_param);
    END io_nested_of_nested;

    PROCEDURE io_nested_of_plsql_table(p_param IN OUT test_return.tt_nested_of_plsql_table) IS
    BEGIN
        test_in_params.in_nested_of_plsql_table(p_param => p_param);
    END io_nested_of_plsql_table;

    PROCEDURE io_nested_of_record_of_nested(p_param IN OUT test_return.tt_nested_of_record_of_nested) IS
    BEGIN
        test_in_params.in_nested_of_record_of_nested(p_param => p_param);
    END io_nested_of_record_of_nested;

    -- 123 VARRAY                                           -- list
    PROCEDURE io_varray(p_param IN OUT test_return.tt_varray) IS
    BEGIN
        test_in_params.in_varray(p_param => p_param);
    END io_varray;

    PROCEDURE io_varray_of_nested(p_param IN OUT test_return.tt_varray_of_nested) IS
    BEGIN
        test_in_params.in_varray_of_nested(p_param => p_param);
    END io_varray_of_nested;

    PROCEDURE io_varray_of_plsql_table(p_param IN OUT test_return.tt_varray_of_plsql_table) IS
    BEGIN
        test_in_params.in_varray_of_plsql_table(p_param => p_param);
    END io_varray_of_plsql_table;

    -- 178 TIME                                             -- datetime.datetime
    --PROCEDURE io_binary_integer(p_param IN OUT BINARY_INTEGER);

    -- 179 TIME WITH TIME ZONE                              -- datetime.datetime
    --PROCEDURE io_binary_integer(p_param IN OUT BINARY_INTEGER);

    -- 180 TIMESTAMP                                        -- datetime.datetime
    PROCEDURE io_timestamp(p_param IN OUT TIMESTAMP) IS
    BEGIN
        test_in_params.in_timestamp(p_param => p_param);
    END io_timestamp;

    -- 181 TIMESTAMP WITH TIME ZONE                         -- datetime.datetime
    --PROCEDURE io_binary_integer(p_param IN OUT BINARY_INTEGER);

    -- 231 TIMESTAMP WITH LOCAL TIME ZONE                   -- datetime.datetime
    --PROCEDURE io_binary_integer(p_param IN OUT BINARY_INTEGER);

    -- 250 PL/SQL RECORD                                    -- tuple - namedtuple
    PROCEDURE io_record(p_param IN OUT test_return.tr_record) IS
    BEGIN
        test_in_params.in_record(p_param => p_param);
    END;

    PROCEDURE io_record_of_records(p_param IN OUT test_return.tr_record_of_records) IS
    BEGIN
        test_in_params.in_record_of_records(p_param => p_param);
    END io_record_of_records;

    PROCEDURE io_record_of_nested(p_param IN OUT test_return.tr_record_of_nested) IS
    BEGIN
        test_in_params.in_record_of_nested(p_param => p_param);
    END io_record_of_nested;

    PROCEDURE io_record_of_plsql_table(p_param IN OUT test_return.tr_record_of_plsql_table) IS
    BEGIN
        test_in_params.in_record_of_plsql_table(p_param => p_param);
    END io_record_of_plsql_table;

    -- 251 PL/SQL TABLE                                     -- mapping
    PROCEDURE io_plsql_table(p_param IN OUT test_return.tt_plsql_table) IS
    BEGIN
        test_in_params.in_plsql_table(p_param => p_param);
    END io_plsql_table;

    PROCEDURE io_plsql_table_of_records(p_param IN OUT test_return.tt_plsql_table_of_records) IS
    BEGIN
        test_in_params.in_plsql_table_of_records(p_param => p_param);
    END io_plsql_table_of_records;

    PROCEDURE io_plsql_table_of_nested(p_param IN OUT test_return.tt_plsql_table_of_nested) IS
    BEGIN
        test_in_params.in_plsql_table_of_nested(p_param => p_param);
    END io_plsql_table_of_nested;

    PROCEDURE io_plsql_table_of_plsql_table(p_param IN OUT test_return.tt_plsql_table_of_plsql_table) IS
    BEGIN
        test_in_params.in_plsql_table_of_plsql_table(p_param => p_param);
    END io_plsql_table_of_plsql_table;

    -- 252 PL/SQL BOOLEAN                                   -- bool
    PROCEDURE io_bool(p_param IN OUT BOOLEAN) IS
    BEGIN
        test_in_params.in_bool(p_param => p_param);
    END;

END test_in_out_params;
