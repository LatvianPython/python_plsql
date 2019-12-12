# 0   placeholder for procedures with no arguments     -- ------||------
# 1   VARCHAR, VARCHAR, STRING                         -- string
# 2   NUMBER, INTEGER, SMALLINT, REAL, FLOAT, DECIMAL  -- float
# 3   BINARY_INTEGER, PLS_INTEGER, POSITIVE, NATURAL   -- int
# 8   LONG                                             -- ??? str or io ???
# 11  ROWID                                            -- str
# 12  DATE                                             -- datetime.datetime
# 23  RAW                                              -- bytes
# 24  LONG RAW                                         -- ??? bytes or byte io ???
# 58  OPAQUE TYPE                                      -- ??? XMLType in Oracle
# 96  CHAR (ANSI FIXED CHAR), CHARACTER                -- str
# 106 MLSLABEL                                         -- ??? only backwards compatibility
# 121 OBJECT                                           -- ???
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


def test_describe_simple_function(plsql):
    result = plsql._describe_procedure("test_synonym_procedure")

    assert result is not None


def test_describe_all_parameters(plsql):
    result = plsql._describe_procedure("test_describe.oracle_datatypes")

    assert result is not None
