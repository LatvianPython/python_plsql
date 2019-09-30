from functools import reduce
from operator import mul


def test_table_type(plsql):
    words = ['aoeu', 'snth', 'qjkx', 'bmwv']

    result = plsql.test_package.compute_agg_length(pt_stringlist=words)

    assert result == sum(len(word) for word in words)


def test_rec_type(plsql):
    record = {
        f'int_{i}': i
        for i
        in range(1, 5)
    }

    result = plsql.test_package.compute_rec_product(pr_rec=record)

    assert result == reduce(mul, record.values())


def test_rec_table(plsql):
    record = {
        'int_1': 1,
        'int_2': 2,
        'int_3': 3,
        'int_4': 4
    }

    table = [record] * 5

    result = plsql.test_package.compute_rec_table(pt_rec=table)

    assert result == reduce(mul, record.values()) * 5
