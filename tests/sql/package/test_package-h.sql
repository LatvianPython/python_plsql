CREATE OR REPLACE PACKAGE test_package AS
    TYPE tt_stringlist IS TABLE OF VARCHAR2(100) INDEX BY BINARY_INTEGER;

    TYPE tt_integers IS TABLE OF INTEGER;

    TYPE tr_rec IS RECORD (
        int_1 INTEGER,
        int_2 INTEGER,
        int_3 INTEGER,
        int_4 INTEGER
        );

    TYPE tt_rec IS TABLE OF tr_rec INDEX BY BINARY_INTEGER;

    "g_int" INTEGER := 5;

    FUNCTION out_integers(p_integer IN INTEGER)
        RETURN tt_integers;

    FUNCTION in_integers(pt_integers IN tt_integers)
        RETURN INTEGER;

    FUNCTION return_record
        RETURN tr_rec;

    FUNCTION return_table_of_recs
        RETURN tt_rec;

    PROCEDURE simple_procedure;

    FUNCTION simple_function(p_int IN INTEGER)
        RETURN INTEGER;

    FUNCTION compute_agg_length(pt_stringlist IN tt_stringlist)
        RETURN INTEGER;

    FUNCTION compute_rec_product(pr_rec IN tr_rec)
        RETURN INTEGER;

    FUNCTION compute_rec_table(pt_rec IN tt_rec)
        RETURN INTEGER;

END test_package;
