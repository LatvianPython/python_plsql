from itertools import accumulate
from operator import mul


def test_list_type(plsql):
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

    assert result == accumulate(record.values(), mul)
