import pytest


@pytest.mark.parametrize(
    "args, kwargs, expected",
    [
        ([1], {}, 111),
        ([1, 2], {}, 103),
        ([1, 2, 3], {}, 6),
        ([1], {"p_third": 3}, 14),
        ([], {"p_first": 1, "p_second": 2}, 103),
    ],
)
def test_arguments_with_defaults_are_optional(plsql, args, kwargs, expected):
    assert plsql.test_matching.with_defaults(*args, **kwargs) == expected


@pytest.mark.parametrize(
    "args, kwargs",
    [
        ([], {}),
        ([], {"p_second": 2}),
        ([1], {"p_first": 1}),
        ([1], {"p_fourth": 4}),
        ([1, 2, 3, 4], {}),
    ],
)
def test_mismatched_arguments_are_rejected(plsql, args, kwargs):
    with pytest.raises(ValueError, match="Arguments do not match subprogram"):
        plsql.test_matching.with_defaults(*args, **kwargs)


@pytest.mark.parametrize(
    "kwargs, expected",
    [({"p_number": 1}, "number"), ({"p_text": "a"}, "text")],
)
def test_overloads_are_matched_by_argument_name(plsql, kwargs, expected):
    assert plsql.test_matching.by_name(**kwargs) == expected


def test_overloads_with_same_arity_are_ambiguous_by_position(plsql):
    with pytest.raises(ValueError, match="matched with too many subprograms"):
        plsql.test_matching.by_name(1)
