# 0   placeholder for procedures with no arguments     -- ------||------
# 1   VARCHAR, VARCHAR, STRING                         -- str
# 2   NUMBER, INTEGER, SMALLINT, REAL, FLOAT, DECIMAL  -- float
# 3   BINARY_INTEGER, PLS_INTEGER, POSITIVE, NATURAL   -- int
# 8   LONG                                             -- str
# 11  ROWID                                            -- str
# 12  DATE                                             -- datetime.datetime
# 23  RAW                                              -- bytes
# 24  LONG RAW                                         -- bytes
# 58  OPAQUE TYPE                                      -- ??? XMLType in Oracle
# 96  CHAR (ANSI FIXED CHAR), CHARACTER                -- str
# 106 MLSLABEL                                         -- ??? only backwards compatibility ???
# 121 OBJECT                                           -- cx_Oracle.Object ???
# 122 NESTED TABLE                                     -- list
# 123 VARRAY                                           -- list
# 178 TIME                                             -- datetime.datetime
# 179 TIME WITH TIME ZONE                              -- datetime.datetime
# 180 TIMESTAMP                                        -- datetime.datetime
# 181 TIMESTAMP WITH TIME ZONE                         -- datetime.datetime
# 231 TIMESTAMP WITH LOCAL TIME ZONE                   -- datetime.datetime
# 250 PL/SQL RECORD                                    -- tuple - namedtuple
# 251 PL/SQL TABLE                                     -- mapping
# 252 PL/SQL BOOLEAN                                   -- bool


def test_describe_simple_procedure(plsql):
    result = plsql._describe_procedure("test_synonym_procedure")
    assert len(list(result)) == 0


def test_describe_procedure_no_arguments(plsql):
    result = plsql._describe_procedure("test_package.simple_procedure")
    assert len(list(result)) == 1


def test_describe_package_function_with_arguments(plsql):
    result = plsql._describe_procedure("test_package.simple_function")
    assert len(list(result)) == 2


def test_describe_function_with_arguments(plsql):
    result = plsql._describe_procedure("simple_function")
    assert len(list(result)) == 2


def test_describe_all_parameters(plsql):
    result = plsql._describe_procedure("test_describe.oracle_datatypes")
    assert len(list(result)) == 27


def test_overloaded_returns_multiple_definitions(plsql):
    result = plsql._describe_procedure("test_overload.to_string")
    assert len(list(result)) == 4
