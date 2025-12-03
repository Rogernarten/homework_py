# interval.py
#
# Yixiao Huang
#
# This file defines the Interval class and supporting utilities for
# representing time intervals measured in seconds. It also implements
# arithmetic and comparison operations with appropriate type checking.

# write your solution here
import functools

def loose_type(func):
    """
    A decorator that permits arithmetic and comparison operations to accept
    either Interval objects or numeric values (int or float). If the operand
    is an Interval, its value is converted into seconds before the wrapped
    function is executed.

    Inputs:
      func (callable): The method being decorated.

    Returns:
      (callable) A wrapper that performs relaxed type handling and then
      dispatches to the wrapped function.

    Error Handling:
      Returns NotImplemented if the operand is not an Interval or numeric type.
    """
    def wrapper(self, other):
        # Return NotImplemented when receiving an unsupported type.
        if not isinstance(other, (Interval, int, float)):
            return NotImplemented

        # Convert Interval operands into their raw seconds representation.
        if isinstance(other, Interval):
            value = other.in_seconds
        else:
            value = other

        return func(self, value)

    return wrapper


def tight_type(func):
    """
    A decorator that restricts operations strictly to Interval operands.
    The operand's internal second value is extracted before the wrapped
    function is called.

    Inputs:
      func (callable): The method being decorated.

    Returns:
      (callable) A wrapper enforcing strict type checking.

    Error Handling:
      Raises InvalidTimeError if the operand is not an Interval.
    """
    def wrapper(self, other):
        # Only Interval instances are allowed.
        if not isinstance(other, Interval):
            raise InvalidTimeError

        return func(self, other.in_seconds)

    return wrapper


class InvalidTimeError(ValueError):
    """
    Raised when a time interval is constructed or operated on with invalid
    values or incompatible operand types.
    Includes negative durations, malformed time strings, or misuse of
    arithmetic operations with Interval.
    """
    def __init__(self, message="Invalid time value or operation."):
        super().__init__(message)


def is_valid_time(*args):
    """
    Checks whether a (seconds, minutes, hours) triple forms a valid,
    non-negative time interval.

    Inputs:
      args (tuple of int): A sequence expected to contain exactly three
        integers corresponding to seconds, minutes, and hours.

    Returns:
      (bool) True if the values form a non-negative time; False otherwise.
    """
    return len(args) == 3 and args[0] + args[1]*60 + args[2]*3600 >= 0


@functools.total_ordering
class Interval:
    """
    Represents a duration of time using an internal count of total seconds.
    Provides conversion properties and supports comparison and arithmetic
    operations through operator overloading.
    """

    def __init__(self, seconds = 0, *, minutes = 0, hours = 0):
        """
        Initializes an Interval using separate hour, minute, and second inputs.

        Inputs:
          seconds (int): The number of seconds.
          minutes (int): The number of minutes.
          hours (int): The number of hours.

        Returns:
          A new Interval instance.

        Error Handling:
          Raises InvalidTimeError if the resulting time is negative or invalid.
        """
        if not is_valid_time(seconds, minutes, hours):
            raise InvalidTimeError("Time Interval length can't be negative!")

        self.t = seconds + minutes*60 + hours*3600


    @classmethod
    def from_string(cls, string:str):
        """
        Constructs an Interval from a string of the form "HH:MM:SS".

        Inputs:
          string (str): A colon-separated representation of hours, minutes,
            and seconds. All components must be non-negative integers.

        Returns:
          (Interval) A new Interval representing the provided time.

        Error Handling:
          Raises InvalidTimeError if the string contains non-digit parts or the
          resulting time is invalid.
        """
        if not all(x.isdigit() for x in string.split(":")):
            raise InvalidTimeError(
                "Invalid format. Expected a time string in the form 'HH:MM:SS' "
                "containing only numeric components."
            )

        if not is_valid_time(*map(int, string.split(":"))):
            raise InvalidTimeError(
                "Invalid time value. The time components must be non-negative and "
                "the string must contain exactly three components."
            )

        h, m, s = map(int, string.split(":"))
        return cls(seconds=s, minutes=m, hours=h)


    @property
    def in_seconds(self):
        """
        Returns the total number of seconds represented by the interval.

        Returns:
          (int) Total seconds.
        """
        return self.t


    @property
    def in_minutes(self):
        """
        Returns the interval value expressed as minutes.

        Returns:
          (float) Total minutes.
        """
        return self.t / 60


    @property
    def in_hours(self):
        """
        Returns the interval value expressed as hours.

        Returns:
          (float) Total hours.
        """
        return self.t / 3600


    def __repr__(self):
        """
        Returns a human-readable string representation of the interval in the
        form H:MM:SS.

        Returns:
          (str) The formatted time string.
        """
        return f"{self.t // 3600}:{self.t % 3600 // 60:02d}:{self.t % 60:02d}"


    @loose_type
    def __eq__(self, other):
        """
        Compares this Interval with another Interval or numeric value
        for equality.

        Inputs:
          other (Interval or number): The object to compare against.

        Returns:
          (bool) True if both values represent the same number of seconds.
        """
        return self.t == other


    @loose_type
    def __lt__(self, other):
        """
        Checks whether this Interval is strictly less than another Interval
        or numeric value.

        Inputs:
          other (Interval or number): The object to compare against.

        Returns:
          (bool) True if this interval is smaller in seconds.
        """
        return self.t < other


    @tight_type
    def __add__(self, other):
        """
        Adds two Intervals together.

        Inputs:
          other (Interval): The interval to add.

        Returns:
          (Interval) A new Interval representing the sum.
        """
        return Interval(self.t + other)


    @tight_type
    def __radd__(self, other):
        """
        Supports addition when the Interval appears on the right-hand side.

        Inputs:
          other (Interval): The interval to add.

        Returns:
          (Interval) A new Interval representing the sum.
        """
        return Interval(self.t + other)


    @tight_type
    def __sub__(self, other):
        """
        Subtracts one Interval from another.

        Inputs:
          other (Interval): The interval to subtract.

        Returns:
          (Interval) A new Interval representing the difference.
        """
        return Interval(self.t - other)


    @tight_type
    def __rsub__(self, other):
        """
        Supports subtraction when the Interval appears on the right-hand side.

        Inputs:
          other (Interval): The interval being subtracted from.

        Returns:
          (Interval) A new Interval representing the difference.
        """
        return Interval(self.t - other)


    @loose_type
    def __mul__(self, other):
        """
        Multiplies this Interval by a numeric scalar or an Interval.

        Inputs:
          other (Interval/ number): The multiplier.

        Returns:
          (Interval) A new Interval scaled by the multiplier.
        """
        return Interval(self.t * other)


    @loose_type
    def __rmul__(self, other):
        """
        Supports scalar multiplication when the Interval appears on the
        right-hand side.

        Inputs:
          other (Interval/ number): The multiplier.

        Returns:
          (Interval) A new Interval scaled by the multiplier.
        """
        return Interval(self.t * other)