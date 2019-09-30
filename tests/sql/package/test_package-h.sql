CREATE OR REPLACE PACKAGE test_package AS
    TYPE tt_stringlist IS TABLE OF VARCHAR2(100) INDEX BY BINARY_INTEGER;


    TYPE tr_rec IS RECORD (
        int_1 INTEGER,
        int_2 INTEGER,
        int_3 INTEGER,
        int_4 INTEGER
        );

    PROCEDURE simple_procedure;

    FUNCTION simple_function(p_int IN INTEGER)
        RETURN INTEGER;

    FUNCTION compute_agg_length(pt_stringlist IN tt_stringlist)
        RETURN INTEGER;

    FUNCTION compute_rec_product(pr_rec IN tr_rec)
        RETURN INTEGER;

END test_package;
