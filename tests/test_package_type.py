from functools import reduce
from operator import mul


def test_table_type(plsql):
    words = ["aoeu", "snth", "qjkx", "bmwv"]

    result = plsql.test_package.compute_agg_length(pt_stringlist=words)

    assert result == sum(len(word) for word in words)


def test_record_as_return_value(plsql):
    result = plsql.test_package.return_record()

    assert result == {"int_1": 1, "int_2": 2, "int_3": 3, "int_4": 4}


def test_table_of_records_as_return_value(plsql):
    result = plsql.test_package.return_table_of_recs()

    assert result == [{"int_1": 1, "int_2": 2, "int_3": 3, "int_4": 4}] * 2


def test_rec_type(plsql):
    record = {"int_1": 1, "int_2": 2, "int_3": 3, "int_4": 4}

    result = plsql.test_package.compute_rec_product(pr_rec=record)

    assert result == reduce(mul, record.values())


def test_rec_table(plsql):
    record = {"int_1": 1, "int_2": 2, "int_3": 3, "int_4": 4}

    table = [record] * 100

    result = plsql.test_package.compute_rec_table(pt_rec=table)

    assert result == reduce(mul, record.values()) * 100
