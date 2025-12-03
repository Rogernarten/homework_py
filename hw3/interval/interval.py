# write your solution here
import functools

def loose_type(func):
    def wrapper(self, other):
        if not isinstance(other, (Interval, int, float)):
            return NotImplemented
        if isinstance(other, Interval):
            value = other.in_seconds
        else:
            value = other
        return func(self, value)
    return wrapper

def tight_type(func):
    def wrapper(self, other):
        if not isinstance(other, Interval):
            raise InvalidTimeError
        return func(self, other.in_seconds)
    return wrapper

class InvalidTimeError(ValueError):
    pass

def is_valid_time(*args):
    return len(args) == 3 and args[0] + args[1]*60 + args[2]*3600 >= 0


@functools.total_ordering
class Interval:
    def __init__(self, seconds = 0, *args, minutes = 0, hours = 0):
        if not is_valid_time(seconds, minutes, hours):
            raise InvalidTimeError
        self.t = seconds + minutes*60 + hours*3600

    @classmethod
    def from_string(cls, string:str):
        if not all(x.isdigit() for x in string.split(":")):
            raise InvalidTimeError
        if not is_valid_time(*map(int, string.split(":"))):
            raise InvalidTimeError
        h,m,s = map(int, string.split(":"))
        return cls(seconds=s, minutes=m, hours= h)

    @property
    def in_seconds(self):
        return self.t

    @property
    def in_minutes(self):
        return self.t / 60

    @property
    def in_hours(self):
        return self.t / 3600

    def __repr__(self):
        return f"{self.t // 3600}:{self.t % 3600 // 60:02d}:{self.t % 60:02d}"

    @loose_type
    def __eq__(self, other):
        return self.t == other

    @loose_type
    def __lt__(self, other):
        return self.t < other

    @tight_type
    def __add__(self, other):
        return Interval(self.t + other)

    @tight_type
    def __radd__(self, other):
        return Interval(self.t + other)

    @tight_type
    def __sub__(self, other):
        return Interval(self.t - other)

    @tight_type
    def __rsub__(self, other):
        return Interval(self.t - other)

    @loose_type
    def __mul__(self, other):
        return Interval(self.t * other)

    @loose_type
    def __rmul__(self, other):
        return Interval(self.t*other)










