CREATE OR REPLACE PACKAGE BODY test_return AS

    -- 0   placeholder for procedures with no arguments     -- ------||------
    -- 1   VARCHAR2, VARCHAR, STRING                        -- str
    FUNCTION ret_varchar
    RETURN VARCHAR2 IS
    BEGIN
        RETURN '42';
    END;

    -- 2   NUMBER, INTEGER, SMALLINT, REAL, FLOAT, DECIMAL  -- float
    FUNCTION ret_number
    RETURN NUMBER IS
    BEGIN
        RETURN 42.42;
    END;

    -- 3   BINARY_INTEGER, PLS_INTEGER, POSITIVE, NATURAL   -- int
    FUNCTION ret_binary_integer
    RETURN BINARY_INTEGER IS
    BEGIN
        RETURN 42;
    END;

    -- 8   LONG ?CLOB?                                      -- str
    FUNCTION ret_clob
    RETURN CLOB IS
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

    -- 252 PL/SQL BOOLEAN                                   -- bool
    FUNCTION ret_bool
    RETURN BOOLEAN IS
    BEGIN
        RETURN TRUE;
    END;


END test_return;
