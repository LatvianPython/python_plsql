def test_dual_single_column(plsql):
    query = '''
SELECT 1 AS test
  FROM dual'''

    assert plsql.query(query).first == 1
    assert list(plsql.query(query).all) == [1]


def test_dual_multiple_column(plsql):
    query = '''
SELECT 1 AS int, '2' AS string, 3.5 AS num FROM dual UNION ALL
SELECT 1 AS int, '2' AS string, 3.5 AS num FROM dual
'''
    first_row = plsql.query(query).first
    all_rows = list(plsql.query(query).all)

    def assert_assumptions(single_row):
        assert len(single_row) == 3
        assert single_row.int == 1
        assert single_row.string == '2'
        assert single_row.num == 3.5

    assert_assumptions(first_row)

    assert len(all_rows) == 2
    for row in all_rows:
        assert_assumptions(row)
        assert row == first_row


def test_larger_query(plsql):
    query = '''
SELECT level 
  FROM dual 
CONNECT BY level <= 1000
'''

    query_generator = plsql.query(query)

    assert query_generator.first == 1

    for row, expected in zip(query_generator.all, range(1, 1000)):
        assert row == expected

    assert len(list(query_generator.all)) == 1000
