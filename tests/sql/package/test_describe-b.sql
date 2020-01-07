-- noinspection SqlDeprecateTypeForFile
-- noinspection SqlUnusedForFile
CREATE OR REPLACE PACKAGE BODY test_describe AS

    PROCEDURE oracle_datatypes(
            p_vc2    IN     VARCHAR2,
            p_vc     OUT    VARCHAR,
            p_str    IN OUT STRING,
            p_long   IN     LONG,
            p_rowid  IN     ROWID,
            p_chara  IN     CHARACTER,
            p_char   IN     CHAR,
            p_raw    IN     RAW,
            p_lraw   IN     LONG RAW,
            p_binint IN     BINARY_INTEGER,
            p_plsint IN     PLS_INTEGER,
            p_bool   IN     BOOLEAN,
            p_nat    IN     NATURAL,
            p_pos    IN     POSITIVE,
            p_posn   IN     POSITIVEN,
            p_natn   IN     NATURALN,
            p_num    IN     NUMBER,
            p_intgr  IN     INTEGER,
            p_int    IN     INT,
            p_small  IN     SMALLINT,
            p_dec    IN     DECIMAL,
            p_real   IN     REAL,
            p_float  IN     FLOAT,
            p_numer  IN     NUMERIC,
            p_dp     IN     DOUBLE PRECISION,
            p_date   IN     DATE,
            p_mls    IN     MLSLABEL) AS
    BEGIN
        NULL;
    END;

END test_describe;
