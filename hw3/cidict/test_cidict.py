from cidict import CIDict
import pytest


def test_is_a_dict():
    cd = CIDict()
    assert isinstance(cd, dict)


def test_constructor_then_get():
    cd = CIDict(first="A", SECOND="B")
    assert cd["first"] == "A"
    assert cd["FIRST"] == "A"
    assert cd["second"] == "B"
    assert cd["SeCoND"] == "B"


def test_set_then_get():
    cd = CIDict()
    cd["first"] = "A"
    cd["SECOND"] = "B"
    assert cd["first"] == "A"
    assert cd["FIRST"] == "A"
    assert cd["second"] == "B"
    assert cd["SeCoND"] == "B"


def test_constructor_get_then_len():
    cd = CIDict(first="A", SECOND="B")
    assert cd["first"] == "A"
    assert cd["FIRST"] == "A"
    assert cd["second"] == "B"
    assert cd["SeCoND"] == "B"
    assert len(cd) == 2


def test_set_then_get_then_len():
    cd = CIDict()
    cd["first"] = "A"
    cd["SECOND"] = "b"
    assert cd["first"] == "A"
    assert cd["FIRST"] == "A"
    assert cd["second"] == "b"
    assert cd["SeCoND"] == "b"
    assert len(cd) == 2


def test_set_many_writes_one():
    cd = CIDict()
    cd["one"] = 1
    cd["ONE"] = 1
    cd["oNe"] = 1
    assert len(cd) == 1


def test_del_ci():
    cd = CIDict()
    cd["one"] = 1
    del cd["ONE"]
    assert len(cd) == 0


def test_no_change_for_non_str():
    cd = CIDict()
    cd[1] = "one"
    cd[2.0] = "two"
    cd[(1, 1, 1)] = "three"
    assert cd[1] == "one"
    assert cd[2.0] == "two"
    assert cd[(1, 1, 1)] == "three"


def test_update_all():
    cd = CIDict(
        a=1,
        B="1",
        c=(
            1,
            2,
        ),
    )
    cd.update_all(lambda x: x * 2)
    assert cd["a"] == 2
    assert cd["b"] == "11"
    assert cd["c"] == (1, 2, 1, 2)


def test_missing_key_access():
    cd = CIDict()
    with pytest.raises(KeyError):
        _ = cd["nonexistent"]


def test_update_with_colliding_keys():
    cd = CIDict(a=1, A=2, b=3)
    assert cd["a"] == 2
    assert cd["A"] == 2
    assert cd["b"] == 3
    assert len(cd) == 2  # Only 'a' and 'b' should remain


def test_update_all_immutable_type():
    cd = CIDict(a="text", b=None, c=(1, 2))
    # Update with a function that would fail on None, e.g., lambda x: x * 2
    cd.update_all(lambda x: x * 2 if x is not None else x)
    assert cd["a"] == "texttext"
    assert cd["b"] is None
    assert cd["c"] == (1, 2, 1, 2)


def test_clear():
    cd = CIDict(a=1, b=2)
    cd.clear()
    assert len(cd) == 0
    with pytest.raises(KeyError):
        _ = cd["a"]


def test_key_iteration():
    cd = CIDict(a=1, A=2, B=3)
    keys = list(cd.keys())
    assert len(keys) == 2
    assert set(keys) == {"a", "b"}  # Expect unique, lowercase representation of keys
