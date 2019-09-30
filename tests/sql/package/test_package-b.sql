CREATE OR REPLACE PACKAGE BODY test_package AS

    PROCEDURE simple_procedure IS
    BEGIN
        NULL;
    END simple_procedure;

    FUNCTION simple_function(p_int IN INTEGER)
        RETURN INTEGER IS
    BEGIN
        RETURN p_int * p_int;
    END simple_function;


    FUNCTION compute_agg_length(pt_stringlist IN tt_stringlist)
        RETURN INTEGER IS
        v_result INTEGER := 0;
    BEGIN

        FOR i IN 1 .. pt_stringlist.COUNT LOOP
            v_result := v_result + LENGTH(pt_stringlist(i));
        END LOOP;

        RETURN v_result;
    END compute_agg_length;



    FUNCTION compute_rec_product(pr_rec IN tr_rec)
        RETURN INTEGER IS
    BEGIN
        RETURN pr_rec.int_1 * pr_rec.int_2 * pr_rec.int_3 * pr_rec.int_4;
    END compute_rec_product;

END test_package;
