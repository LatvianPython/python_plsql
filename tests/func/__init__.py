# ROWID of DUAL differs between databases
class _DualRowid:
    def __repr__(self):
        return "DUAL_ROWID"


DUAL_ROWID = _DualRowid()


def resolve(plsql, value):
    if value is DUAL_ROWID:
        return plsql.query("SELECT ROWID FROM dual").first
    return value


# OUT CHAR is blank-padded to the bind buffer size, which differs between drivers
class BlankPadded:
    def __init__(self, value: str):
        self.value = value

    def __eq__(self, other):
        return isinstance(other, str) and other.rstrip(" ") == self.value

    def __repr__(self):
        return f"BlankPadded({self.value!r})"
