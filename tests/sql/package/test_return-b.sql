-- noinspection SqlDeprecateType

CREATE OR REPLACE PACKAGE BODY test_return AS

    -- 0   placeholder for procedures with no arguments     -- ------||------
    -- 1   VARCHAR2, VARCHAR, STRING                        -- str
    FUNCTION ret_varchar2
    RETURN VARCHAR2 IS
        v_varchar2 VARCHAR2(2) := '42';
    BEGIN
        RETURN v_varchar2;
    END ret_varchar2;

    FUNCTION ret_varchar
    RETURN VARCHAR IS
        v_varchar VARCHAR2(2) := '42';
    BEGIN
        RETURN v_varchar;
    END ret_varchar;

    FUNCTION ret_string
    RETURN STRING IS
        v_string STRING(2) := '42';
    BEGIN
        RETURN v_string;
    END ret_string;

    -- 2   NUMBER, INTEGER, SMALLINT, REAL, FLOAT, DECIMAL  -- float
    FUNCTION ret_number
    RETURN NUMBER IS
        v_number NUMBER := 42.42;
    BEGIN
        RETURN v_number;
    END ret_number;

    FUNCTION ret_integer
    RETURN INTEGER IS
        v_integer INTEGER := 42;
    BEGIN
        RETURN v_integer;
    END ret_integer;

    FUNCTION ret_smallint
    RETURN SMALLINT IS
        v_smallint SMALLINT := 42;
    BEGIN
        RETURN v_smallint;
    END ret_smallint;

    FUNCTION ret_real
    RETURN REAL IS
        v_real REAL := 42.42;
    BEGIN
        RETURN v_real;
    END ret_real;

    FUNCTION ret_float
    RETURN FLOAT IS
        v_float FLOAT := 42.42;
    BEGIN
        RETURN v_float;
    END ret_float;

    FUNCTION ret_numeric
    RETURN NUMERIC IS
        v_numeric NUMERIC := 42;
    BEGIN
        RETURN v_numeric;
    END ret_numeric;

    FUNCTION ret_decimal
    RETURN DECIMAL IS
        v_decimal DECIMAL := 42;
    BEGIN
        RETURN v_decimal;
    END ret_decimal;

    -- 3   BINARY_INTEGER, PLS_INTEGER, POSITIVE, NATURAL   -- int
    FUNCTION ret_binary_integer
    RETURN BINARY_INTEGER IS
    BEGIN
        RETURN 42;
    END;

    FUNCTION ret_pls_integer
    RETURN PLS_INTEGER IS
    BEGIN
        RETURN 42;
    END;

    FUNCTION ret_positive
    RETURN POSITIVE IS
    BEGIN
        RETURN 42;
    END;

    FUNCTION ret_natural
    RETURN NATURAL IS
    BEGIN
        RETURN 42;
    END;

    -- 8   LONG ?CLOB?                                      -- str
    FUNCTION ret_clob
    RETURN CLOB IS
    BEGIN
        RETURN '42';
    END;

    FUNCTION ret_long
    RETURN LONG IS
    BEGIN
        RETURN '42';
    END;

    -- 11  ROWID                                            -- str
    FUNCTION ret_rowid
    RETURN ROWID IS
        v_rowid ROWID;
    BEGIN
        SELECT ROWID
          INTO v_rowid
          FROM dual;

        RETURN v_rowid;
    END;

    -- 12  DATE                                             -- datetime.datetime
    FUNCTION ret_date
    RETURN DATE IS
    BEGIN
        RETURN TO_DATE('20.12.2019', 'dd.mm.yyyy');
    END;

    -- 23  RAW                                              -- bytes
    FUNCTION ret_raw
    RETURN RAW IS
    BEGIN
        RETURN HEXTORAW('3432');
    END;

    -- 24  LONG RAW                                         -- bytes
    FUNCTION ret_long_raw
    RETURN LONG RAW IS
    BEGIN
        RETURN HEXTORAW('3432');
    END;

    -- 58  OPAQUE TYPE                                      -- ??? XMLType in Oracle
    --FUNCTION ret_binary_integer
    --RETURN BINARY_INTEGER;

    -- 96  CHAR (ANSI FIXED CHAR), CHARACTER                -- str
    FUNCTION ret_char
    RETURN CHAR IS
    BEGIN
        RETURN '42';
    END;

    FUNCTION ret_character
    RETURN CHARACTER IS
    BEGIN
        RETURN '42';
    END;

    -- 106 MLSLABEL                                         -- ??? only backwards compatibility ???
    --FUNCTION ret_binary_integer
    --RETURN BINARY_INTEGER;

    -- 121 OBJECT                                           -- cx_Oracle.Object ???
    --FUNCTION ret_binary_integer
    --RETURN BINARY_INTEGER;

    -- 122 NESTED TABLE                                     -- list
    FUNCTION ret_nested
    RETURN tt_nested IS
        vt_nested tt_nested := tt_nested();
    BEGIN
        FOR v_i IN 1 .. 10 LOOP
            vt_nested.extend;
            vt_nested(v_i) := v_i * 2;
        END LOOP;
        RETURN vt_nested;
    END ret_nested;

    FUNCTION ret_nested_of_records
    RETURN tt_nested_of_records IS
        vt_nested_of_records tt_nested_of_records := tt_nested_of_records();
    BEGIN
        FOR v_i IN 1 .. 10 LOOP
            vt_nested_of_records.extend;
            vt_nested_of_records(v_i) := ret_record;
        END LOOP;
        RETURN vt_nested_of_records;
    END ret_nested_of_records;

    FUNCTION ret_nested_of_nested
    RETURN tt_nested_of_nested IS
        vt_nested_of_nested tt_nested_of_nested := tt_nested_of_nested();
    BEGIN
        FOR v_i IN 1 .. 10 LOOP
            vt_nested_of_nested.extend;
            vt_nested_of_nested(v_i) := ret_nested;
        END LOOP;
        RETURN vt_nested_of_nested;
    END ret_nested_of_nested;

    FUNCTION ret_nested_of_plsql_table
    RETURN tt_nested_of_plsql_table IS
        vt_nested_of_plsql_table tt_nested_of_plsql_table := tt_nested_of_plsql_table();
    BEGIN
        FOR v_i IN 1 .. 10 LOOP
            vt_nested_of_plsql_table.extend;
            vt_nested_of_plsql_table(v_i) := ret_plsql_table;
        END LOOP;
        RETURN vt_nested_of_plsql_table;
    END ret_nested_of_plsql_table;

    FUNCTION ret_nested_of_record_of_nested
    RETURN tt_nested_of_record_of_nested IS
        vt_nested_of_record_of_nested tt_nested_of_record_of_nested := tt_nested_of_record_of_nested();
    BEGIN
        FOR v_i IN 1 .. 10 LOOP
            vt_nested_of_record_of_nested.extend;
            vt_nested_of_record_of_nested(v_i) := ret_record_of_nested;
        END LOOP;
        return vt_nested_of_record_of_nested;
    END ret_nested_of_record_of_nested;

    -- 123 VARRAY                                           -- list
    FUNCTION ret_varray
    RETURN tt_varray IS
    BEGIN
        RETURN tt_varray(10, 9, 8, 7, 6, 5, 4, 3, 2, 1);
    END ret_varray;

    FUNCTION ret_varray_of_nested
    RETURN tt_varray_of_nested IS
        vt_varray_of_nested tt_varray_of_nested := tt_varray_of_nested();
    BEGIN
        FOR v_i IN 1 .. 10 LOOP
            vt_varray_of_nested.extend;
            vt_varray_of_nested(v_i) := ret_nested;
        END LOOP;
        RETURN vt_varray_of_nested;
    END ret_varray_of_nested;

    FUNCTION ret_varray_of_plsql_table
    RETURN tt_varray_of_plsql_table IS
        vt_varray_of_plsql_table tt_varray_of_plsql_table := tt_varray_of_plsql_table();
    BEGIN
        FOR v_i IN 1 .. 10 LOOP
            vt_varray_of_plsql_table.extend;
            vt_varray_of_plsql_table(v_i) := ret_plsql_table;
        END LOOP;
        RETURN vt_varray_of_plsql_table;
    END ret_varray_of_plsql_table;

    -- 178 TIME                                             -- datetime.datetime
    --FUNCTION ret_binary_integer
    --RETURN BINARY_INTEGER;

    -- 179 TIME WITH TIME ZONE                              -- datetime.datetime
    --FUNCTION ret_binary_integer
    --RETURN BINARY_INTEGER;

    -- 180 TIMESTAMP                                        -- datetime.datetime
    FUNCTION ret_timestamp
    RETURN TIMESTAMP IS
    BEGIN
        RETURN to_timestamp(ret_date);
    END ret_timestamp;

    -- 181 TIMESTAMP WITH TIME ZONE                         -- datetime.datetime
    --FUNCTION ret_binary_integer
    --RETURN BINARY_INTEGER;

    -- 231 TIMESTAMP WITH LOCAL TIME ZONE                   -- datetime.datetime
    --FUNCTION ret_binary_integer
    --RETURN BINARY_INTEGER;

    -- 250 PL/SQL RECORD                                    -- tuple - namedtuple
    FUNCTION ret_record
    RETURN tr_record IS
        vr_record tr_record;
    BEGIN
        vr_record.t_int_1 := 42;
        vr_record.t_int_2 := 84;
        vr_record.t_int_3 := 126;
        RETURN vr_record;
    END;

    FUNCTION ret_record_of_records
    RETURN tr_record_of_records IS
        vr_record_of_records tr_record_of_records;
    BEGIN
        vr_record_of_records.t_int_1 := 42;
        vr_record_of_records.t_rec_2 := ret_record;
        vr_record_of_records.t_rec_3 := ret_record;
        RETURN vr_record_of_records;
    END ret_record_of_records;

    FUNCTION ret_record_of_nested
    RETURN tr_record_of_nested IS
        vr_record_of_nested tr_record_of_nested;
    BEGIN
        vr_record_of_nested.t_int_1 := 42;
        vr_record_of_nested.t_nes_2 := ret_nested;
        vr_record_of_nested.t_nes_3 := ret_nested;
        RETURN vr_record_of_nested;
    END ret_record_of_nested;

    FUNCTION ret_record_of_plsql_table
    RETURN tr_record_of_plsql_table IS
        vr_record_of_plsql_table tr_record_of_plsql_table;
    BEGIN
        vr_record_of_plsql_table.t_int_1 := 42;
        vr_record_of_plsql_table.t_pls_2 := ret_plsql_table;
        vr_record_of_plsql_table.t_pls_3 := ret_plsql_table;
        RETURN vr_record_of_plsql_table;
    END ret_record_of_plsql_table;

    -- 251 PL/SQL TABLE                                     -- mapping
    FUNCTION ret_plsql_table
    RETURN tt_plsql_table IS
        vt_plsql_table tt_plsql_table;
    BEGIN
        FOR v_i IN 1 .. 10 LOOP
            vt_plsql_table(v_i) := v_i;
        END LOOP;
        RETURN vt_plsql_table;
    END ret_plsql_table;

    FUNCTION ret_plsql_table_of_records
    RETURN tt_plsql_table_of_records IS
        vt_plsql_table_of_records tt_plsql_table_of_records;
    BEGIN
        FOR v_i IN 1 .. 10 LOOP
            vt_plsql_table_of_records(v_i) := ret_record;
        END LOOP;
        RETURN vt_plsql_table_of_records;
    END ret_plsql_table_of_records;

    FUNCTION ret_plsql_table_of_nested
    RETURN tt_plsql_table_of_nested IS
        vt_plsql_table_of_nested tt_plsql_table_of_nested;
    BEGIN
        FOR v_i IN 1 .. 10 LOOP
            vt_plsql_table_of_nested(v_i) := ret_nested;
        END LOOP;
        RETURN vt_plsql_table_of_nested;
    END ret_plsql_table_of_nested;

    FUNCTION ret_plsql_table_of_plsql_table
    RETURN tt_plsql_table_of_plsql_table IS
        vt_plsql_table_of_plsql_table tt_plsql_table_of_plsql_table := tt_plsql_table_of_plsql_table();
    BEGIN
        FOR v_i IN 1 .. 10 LOOP
            vt_plsql_table_of_plsql_table(v_i) := ret_plsql_table;
        END LOOP;
        RETURN vt_plsql_table_of_plsql_table;
    END ret_plsql_table_of_plsql_table;

    -- 252 PL/SQL BOOLEAN                                   -- bool
    FUNCTION ret_bool
    RETURN BOOLEAN IS
    BEGIN
        RETURN TRUE;
    END;


END test_return;
