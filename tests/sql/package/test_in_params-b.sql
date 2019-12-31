-- noinspection SqlDeprecateType

CREATE OR REPLACE PACKAGE BODY test_in_params AS

    PROCEDURE err(p_throw IN BOOLEAN) IS
    BEGIN
        IF p_throw THEN
            raise_application_error(-20001, 'not equal');
        END IF;
    END err;

    -- 0   placeholder for procedures with no arguments     -- ------||------
    -- 1   VARCHAR2, VARCHAR, STRING                        -- str
    PROCEDURE in_varchar2(p_param IN VARCHAR2) IS
    BEGIN
        err(p_param != test_return.ret_varchar2);
    END in_varchar2;

    PROCEDURE in_varchar(p_param IN VARCHAR) IS
    BEGIN
        err(p_param != test_return.ret_varchar);
    END in_varchar;

    PROCEDURE in_string(p_param IN STRING) IS
    BEGIN
        err(p_param != test_return.ret_string);
    END in_string;

    -- 2   NUMBER, INTEGER, SMALLINT, REAL, FLOAT, DECIMAL  -- float
    PROCEDURE in_number(p_param IN NUMBER) IS
    BEGIN
        err(p_param != test_return.ret_number);
    END in_number;

    PROCEDURE in_integer(p_param IN INTEGER) IS
    BEGIN
        err(p_param != test_return.ret_integer);
    END in_integer;

    PROCEDURE in_smallint(p_param IN SMALLINT) IS
    BEGIN
        err(p_param != test_return.ret_smallint);
    END in_smallint;

    PROCEDURE in_real(p_param IN REAL) IS
    BEGIN
        err(p_param != test_return.ret_real);
    END in_real;

    PROCEDURE in_float(p_param IN FLOAT) IS
    BEGIN
        err(p_param != test_return.ret_float);
    END in_float;

    PROCEDURE in_numeric(p_param IN NUMERIC) IS
    BEGIN
        err(p_param != test_return.ret_numeric);
    END in_numeric;

    PROCEDURE in_decimal(p_param IN DECIMAL) IS
    BEGIN
        err(p_param != test_return.ret_decimal);
    END in_decimal;

    -- 3   BINARY_INTEGER, PLS_INTEGER, POSITIVE, NATURAL   -- int
    PROCEDURE in_binary_integer(p_param IN BINARY_INTEGER) IS
    BEGIN
        err(p_param != test_return.ret_binary_integer);
    END;

    PROCEDURE in_pls_integer(p_param IN PLS_INTEGER) IS
    BEGIN
        err(p_param != test_return.ret_pls_integer);
    END;

    PROCEDURE in_positive(p_param IN POSITIVE) IS
    BEGIN
        err(p_param != test_return.ret_positive);
    END;

    PROCEDURE in_natural(p_param IN NATURAL) IS
    BEGIN
        err(p_param != test_return.ret_natural);
    END;

    -- 8   LONG ?CLOB?                                      -- str
    PROCEDURE in_clob(p_param IN CLOB) IS
    BEGIN
        err(p_param != test_return.ret_clob);
    END;

    PROCEDURE in_long(p_param IN LONG) IS
    BEGIN
        err(p_param != test_return.ret_long);
    END;

    -- 11  ROWID                                            -- str
    PROCEDURE in_rowid(p_param IN ROWID) IS
    BEGIN
        err(p_param != test_return.ret_rowid);
    END;

    -- 12  DATE                                             -- datetime.datetime
    PROCEDURE in_date(p_param IN DATE) IS
    BEGIN
        err(p_param != test_return.ret_date);
    END;

    -- 23  RAW                                              -- bytes
    PROCEDURE in_raw(p_param IN RAW) IS
    BEGIN
        err(p_param != test_return.ret_raw);
    END;

    -- 24  LONG RAW                                         -- bytes
    PROCEDURE in_long_raw(p_param IN LONG RAW) IS
    BEGIN
        err(p_param != test_return.ret_long_raw);
    END;

    -- 58  OPAQUE TYPE                                      -- ??? XMLType in Oracle
    --PROCEDURE in_binary_integer(p_param IN BINARY_INTEGER);

    -- 96  CHAR (ANSI FIXED CHAR), CHARACTER                -- str
    PROCEDURE in_char(p_param IN CHAR) IS
    BEGIN
        err(p_param != test_return.ret_char);
    END;

    PROCEDURE in_character(p_param IN CHARACTER) IS
    BEGIN
        err(p_param != test_return.ret_character);
    END;

    -- 106 MLSLABEL                                         -- ??? only backwards compatibility ???
    --PROCEDURE in_binary_integer(p_param IN BINARY_INTEGER);

    -- 121 OBJECT                                           -- cx_Oracle.Object ???
    --PROCEDURE in_binary_integer(p_param IN BINARY_INTEGER);

    -- 122 NESTED TABLE                                     -- list
    PROCEDURE in_nested(p_param IN tt_nested) IS
    BEGIN
        NULL;
    END in_nested;

    PROCEDURE in_nested_of_records(p_param IN tt_nested_of_records) IS
    BEGIN
        NULL;
    END in_nested_of_records;

    PROCEDURE in_nested_of_nested(p_param IN tt_nested_of_nested) IS
    BEGIN
        NULL;
    END in_nested_of_nested;

    PROCEDURE in_nested_of_plsql_table(p_param IN tt_nested_of_plsql_table) IS
    BEGIN
        NULL;
    END in_nested_of_plsql_table;

    PROCEDURE in_nested_of_record_of_nested(p_param IN tt_nested_of_record_of_nested) IS
    BEGIN
        NULL;
    END in_nested_of_record_of_nested;

    -- 123 VARRAY                                           -- list
    PROCEDURE in_varray(p_param IN tt_varray) IS
    BEGIN
        NULL;
    END in_varray;

    PROCEDURE in_varray_of_nested(p_param IN tt_varray_of_nested) IS
    BEGIN
        NULL;
    END in_varray_of_nested;

    PROCEDURE in_varray_of_plsql_table(p_param IN tt_varray_of_plsql_table) IS
    BEGIN
        NULL;
    END in_varray_of_plsql_table;

    -- 178 TIME                                             -- datetime.datetime
    --PROCEDURE in_binary_integer(p_param IN BINARY_INTEGER);

    -- 179 TIME WITH TIME ZONE                              -- datetime.datetime
    --PROCEDURE in_binary_integer(p_param IN BINARY_INTEGER);

    -- 180 TIMESTAMP                                        -- datetime.datetime
    PROCEDURE in_timestamp(p_param IN TIMESTAMP) IS
    BEGIN
        err(p_param != test_return.ret_timestamp);
    END in_timestamp;

    -- 181 TIMESTAMP WITH TIME ZONE                         -- datetime.datetime
    --PROCEDURE in_binary_integer(p_param IN BINARY_INTEGER);

    -- 231 TIMESTAMP WITH LOCAL TIME ZONE                   -- datetime.datetime
    --PROCEDURE in_binary_integer(p_param IN BINARY_INTEGER);

    -- 250 PL/SQL RECORD                                    -- tuple - namedtuple
    PROCEDURE in_record(p_param IN tr_record) IS
    BEGIN
        NULL;
    END;

    PROCEDURE in_record_of_records(p_param IN tr_record_of_records) IS
    BEGIN
        NULL;
    END in_record_of_records;

    PROCEDURE in_record_of_nested(p_param IN tr_record_of_nested) IS
    BEGIN
        NULL;
    END in_record_of_nested;

    PROCEDURE in_record_of_plsql_table(p_param IN tr_record_of_plsql_table) IS
    BEGIN
        NULL;
    END in_record_of_plsql_table;

    -- 251 PL/SQL TABLE                                     -- mapping
    PROCEDURE in_plsql_table(p_param IN tt_plsql_table) IS
    BEGIN
        NULL;
    END in_plsql_table;

    PROCEDURE in_plsql_table_of_records(p_param IN tt_plsql_table_of_records) IS
    BEGIN
        NULL;
    END in_plsql_table_of_records;

    PROCEDURE in_plsql_table_of_nested(p_param IN tt_plsql_table_of_nested) IS
    BEGIN
        NULL;
    END in_plsql_table_of_nested;

    PROCEDURE in_plsql_table_of_plsql_table(p_param IN tt_plsql_table_of_plsql_table) IS
    BEGIN
        NULL;
    END in_plsql_table_of_plsql_table;

    -- 252 PL/SQL BOOLEAN                                   -- bool
    PROCEDURE in_bool(p_param IN BOOLEAN) IS
    BEGIN
        err(p_param != test_return.ret_bool);
    END;


END test_in_params;
