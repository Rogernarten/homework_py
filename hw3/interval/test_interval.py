import math
import pytest
from interval import Interval, InvalidTimeError


def test_invalid_time_error():
    # Ensure InvalidTimeError is a subclass of ValueError
    assert issubclass(InvalidTimeError, ValueError)


def test_interval_negative_error():
    with pytest.raises(InvalidTimeError):
        Interval(-1)
    with pytest.raises(InvalidTimeError):
        Interval(minutes=-1)
    with pytest.raises(InvalidTimeError):
        Interval(hours=-1)


def test_interval_initialization_and_equals():
    # this test has to rely on both methods working
    assert Interval() == Interval(0)
    assert Interval(50) == Interval(seconds=50)
    assert Interval(10, minutes=1) == Interval(70)
    assert Interval(seconds=1, hours=1) == Interval(3601)
    assert Interval(hours=1, minutes=1, seconds=1) == Interval(3661)


def test_not_equals():
    assert Interval() != Interval(1)
    assert Interval(30) != Interval(seconds=50)
    assert Interval(minutes=1) != Interval(70)
    assert Interval(hours=1) != Interval()


def test_from_string_valid():
    assert Interval.from_string("0:00:50") == Interval(50)
    assert Interval.from_string("0:01:10") == Interval(70)
    assert Interval.from_string("1:00:01") == Interval(3601)
    assert Interval.from_string("100:00:01") == Interval(360001)


def test_from_string_invalid():
    with pytest.raises(InvalidTimeError):
        Interval.from_string("invalid")
    with pytest.raises(InvalidTimeError):
        Interval.from_string("1:2:3:4")
    with pytest.raises(InvalidTimeError):
        Interval.from_string("abc:def:ghi")
    # it is OK if times like 12:3:4 are accepted, but not required


def test_repr():
    assert repr(Interval(seconds=121)) == "0:02:01"
    assert repr(Interval()) == "0:00:00"
    assert repr(Interval(hours=200)) == "200:00:00"


def test_less_than():
    assert Interval(0) < Interval(1) < Interval(86400)


def test_greater_than():
    assert Interval(86400) > Interval(1) > Interval(0)


def test_less_than_eq():
    assert Interval(0) <= Interval(0) <= Interval(500) <= Interval(500)


def test_greater_than_eq():
    assert Interval(500) >= Interval(500) >= Interval(0) >= Interval(0)


def test_addition():
    assert Interval(10) + Interval(20) == Interval(30)
    assert Interval(60) + Interval(3600) == Interval(hours=1, minutes=1)
    assert Interval(hours=1) + Interval(hours=1) == Interval(hours=2)
    assert Interval(minutes=30) + Interval(minutes=30) == Interval(hours=1)


def test_subtraction():
    assert Interval(hours=1) - Interval(minutes=59) == Interval(minutes=1)
    assert Interval(minutes=1) - Interval(seconds=59) == Interval(1)


def test_sub_negative():
    with pytest.raises(InvalidTimeError):
        _ = Interval() - Interval(minutes=10)


def test_addition_valueerror():
    with pytest.raises(ValueError):
        _ = Interval(10) + 5


def test_subtraction_valueerror():
    with pytest.raises(ValueError):
        _ = Interval(10) - 5


def test_in_seconds():
    assert Interval(5).in_seconds == 5
    assert Interval(minutes=1).in_seconds == 60
    assert Interval(hours=1).in_seconds == 3600
    assert Interval(hours=1, minutes=1, seconds=3).in_seconds == 3663
    assert Interval(hours=1, seconds=5).in_seconds == 3605


def test_in_minutes():
    assert math.isclose(Interval(30).in_minutes, 0.5)
    assert math.isclose(Interval(minutes=1).in_minutes, 1.0)
    assert math.isclose(Interval(hours=1).in_minutes, 60.0)
    assert math.isclose(Interval(hours=1, minutes=1, seconds=15).in_minutes, 61.25)


def test_in_hours():
    assert math.isclose(Interval(360).in_hours, 0.1)
    assert math.isclose(Interval(minutes=10).in_hours, 1 / 6)
    assert math.isclose(Interval(hours=1).in_hours, 1)
    assert math.isclose(Interval(hours=1, minutes=30).in_hours, 1.5)


def test_multiplication():
    assert Interval(10) * 5 == Interval(50)
    assert Interval(20) * 3 == Interval(minutes=1)


def test_multiplication_reverse():
    assert 60 * 60 * Interval(1) == Interval(hours=1)


def test_multiplication_valueerror():
    with pytest.raises(InvalidTimeError):
        _ = Interval(10) * -5
    with pytest.raises(InvalidTimeError):
        _ = -5 * Interval(10)
