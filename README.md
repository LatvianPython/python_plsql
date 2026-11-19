# Description

Makes testing PL/SQL easier by providing a simple way to call it from an easy to use language

# How to use this right now?

What you need is the `python_plsql` package (`pip install .` from this repository), the [python-oracledb](https://python-oracledb.readthedocs.io/) package (`pip install oracledb`) and an Oracle database you can point this script to.

Thin mode (the default) decodes PL/SQL collections of `PLS_INTEGER`/`BINARY_INTEGER` as booleans. To avoid that, install [Oracle Instant Client](https://www.oracle.com/database/technologies/instant-client.html) and pass its directory as `Database(..., oracle_client_dir=...)` to use thick mode.

# Running the tests

Start an Oracle Database Free container (creates `TEST_USER` on first start), then fill in `tests/database.ini`:

```
docker compose up -d
pip install -e ".[test]"
pytest
```

# Example(s)

Hopefully if all goes well you will be able to call most of the PL/SQL code from Python
```Python
>>>plsql = Database(...)
>>>plsql.simple_function(p_int=5)
10
```

Refer to tests for what is being supported right now, it is not a lot, but enough for a proof of concept (Creating an easy way to call PL/SQL from Python)
