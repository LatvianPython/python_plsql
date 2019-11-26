CREATE OR REPLACE PACKAGE BODY test_package AS

    FUNCTION return_record
        RETURN tr_rec IS
        vr_rec tr_rec;
    BEGIN
        vr_rec.int_1 := 1;
        vr_rec.int_2 := 2;
        vr_rec.int_3 := 3;
        vr_rec.int_4 := 4;
        RETURN vr_rec;
    END return_record;

    FUNCTION return_table_of_recs
        RETURN tt_rec IS
        vt_rec tt_rec;
    BEGIN
        FOR v_i IN 1 .. 2 LOOP
            vt_rec(v_i) := return_record;
        END LOOP;
        RETURN vt_rec;
    END;

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

        FOR i IN pt_stringlist.FIRST .. pt_stringlist.LAST LOOP
            v_result := v_result + LENGTH(pt_stringlist(i));
        END LOOP;

        RETURN v_result;
    END compute_agg_length;


    FUNCTION compute_rec_product(pr_rec IN tr_rec)
        RETURN INTEGER IS
    BEGIN
        RETURN pr_rec.int_1 * pr_rec.int_2 * pr_rec.int_3 * pr_rec.int_4;
    END compute_rec_product;


    FUNCTION compute_rec_table(pt_rec IN tt_rec)
        RETURN INTEGER IS
        v_result INTEGER := 0;
    BEGIN
        FOR i IN pt_rec.FIRST .. pt_rec.LAST LOOP
            v_result := v_result + (pt_rec(i).int_1 * pt_rec(i).int_2 * pt_rec(i).int_3 * pt_rec(i).int_4);
        END LOOP;
        RETURN v_result;
    EXCEPTION
        WHEN NO_DATA_FOUND THEN
            RETURN pt_rec.COUNT;
    END compute_rec_table;

END test_package;
