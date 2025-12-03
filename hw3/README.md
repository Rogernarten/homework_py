# Homework #3

Make sure you run `uv sync` on this project after you clone this repository.

## AI Policy Reminder

You can use the internet, including AI engines, but you must use them similar to if you had a smart friend to work with:

1. You CAN ask high-level questions:
   For example, "Does Python have a built-in ability to read JSON files, or do I need to import something?"

2. You CANNOT ask for the solution code by entering this assignment as a prompt.
   For example, "Generate a Python program to read the given files and generate the following output: .." is NOT PERMITTED

3. You MAY ask for SAMPLE code to demonstrate various examples of Python usage
   For example, "Can you show me a short example of how to read lines from a file on disk?"
   This is acceptable because you're asking for help on a general principle, from which you must
   still apply to the specifics of this assignment.

4. Whenever you learn something new from AI that you then apply to your work, you MUST CITE the exact prompt(s) and LLM engine that you used and what you learned from it that you felt helped you with this assignment.

For convenience, you can update this README.md file with your citations.

## AI Usage & Citations

I consulted ChatGPT (OpenAI GPT-5.1, December 2025 version) for help on the following high-level concepts:

1. Understanding how to override __setitem__, __getitem__, and __delitem__ in a subclass of dict. 
2. Clarifying how decorators such as @functools.total_ordering work conceptually.
3. Asking how to improve error messages for the InvalidTimeError.

I did not request or receive any complete solutions for the homework problems.
All implementation logic, class structure, and debugging were done by myself.

## Assignment Objectives

This assignment will give you practice writing classes in Python, designing an OOP class hierarchy, and using dunder methods to overload operators.

## Assignment Instructions

There are two different problems in this homework assignment:

1. Implement a specialization of a built-in Python type
2. Implement a completely new Python type that looks and feels like a built-in type

## Problem 1: CIDict

For this part, you need to implement a `CIDict` subclass of `dict` that implements the following:

- `__setitem__`, `__getitem__`, and `__delitem__` should treat string keys as case-insensitive.  Any non-string key should not be modified.
- An `update_all` method that takes a function and updates all values in the dictionary using it, as shown here:

```
>>> cd = CIDict(a=1, b=2, c=3)
>>> cd.update_all(lambda x: x + 1)
>>> for k, v in cd:
...    print(k, v)
a 2
b 3
c 4

```

**Important: This class should subclass `dict`, it should not add any attributes. The purpose of this assignment is considering how subclasses of built-in types work.**

- To ensure that the `CIDict` constructor is case-insensitive, you will need to implement it using your `__setitem__` method. It should have the signature `__init__(self, **kwargs)` and initialize the dictionary accordingly.

Write your implementation in `cidict/cidict.py`.

To test: `uv run pytest cidict/`


## Problem 2: Interval

For this problem, you will be writing an `Interval` class representing a span of time.

The entire implementation should be inside `interval/interval.py`.

You can run the tests with `uv run pytest interval/`.

**You should not use datetime in your implementation.**

0) First, define a `InvalidTimeError` that inherits from `ValueError`.

Next, you will create an `Interval` class with the following methods:

1) A constructor that takes a single optional positional argument 'seconds'. It should have two keyword-only arguments: 'minutes', and 'hours'.

Examples:

```python
Interval()                      # 0:00:00 (0 seconds)
Interval(50)                    # 0:00:50 (50 seconds)
Interval(10, minutes=1)         # 0:01:10 (70 seconds)
Interval(seconds=1, hours=1)    # 1:00:01 (3601 seconds)
```

You should store the data however you decide is most appropriate.

Any attempt to create a negative interval should raise a `InvalidTimeError`.

2) An "alternate constructor" named `from_string` implemented using `@classmethod` that takes a HHH:MM:SS string as input.

```python
Interval.from_string("0:00:50")   # 50 seconds
Interval.from_string("0:01:10")   # 70 seconds
Interval.from_string("1:00:01")   # 3601 seconds
Interval.from_string(7)
```

The format is further described below (step 4, `__repr__`), if `from_string` receives a value it cannot parse it should raise `InvalidTimeError`

3) Three **read-only properties**:

- `in_seconds` - Return interval converted to seconds as an integer.
- `in_minutes` - Return interval converted to minutes as floating point number.
- `in_hours` - Return interval converted to hours as floating point number.

These return the **entire interval** expressed in the given unit, for example:

```python
Interval(minutes=1).in_seconds == 60              # 1 minutes = 60 seconds
Interval(hours=1).in_minutes == 60.0              # 1 hour = 60 minutes
Interval(30).in_minutes == 0.5                    # 30 seconds = half a minute
Interval(hours=2, minutes=15).in_hours == 2.25    # 2:15 is 2.25 hours
```

If the format is invalid, this method should raise an `InvalidTimeError` with a helpful error message.

4) A `__repr__` that returns the Interval in HHH:MM:SS format.

**Note**: For both parts 2 & 4 below, the expected format is `HHH:MM:SS`:

- `HHH`: Number of hours. Unlike MM and SS this value is not zero-padded. See examples.
- `MM`: Number of remainder minutes (not counting those already counted as hours). Zero-padded as to always take two digits.
- `SS`: Number of remainder seconds (not counting those already counted as minutes) Zero-padded as well.

Examples are helpful here:

```python
repr(Interval(seconds=121)) == "0:02:01"
repr(Interval()) == "0:00:00"   # hours are not zero padded
repr(Interval(hours=200)) == "200:00:00"   # hours can exceed two digits
```

5) Intervals should be comparable with `==`, `<`, `>`, `>=`, `<=`, and `!=`.

These should work as one would expect. 

`Interval(0) < Interval(seconds=1) < Interval(hours=2) < Interval(days=1)`

You may use the **class decorator** `@functools.total_ordering`: <https://docs.python.org/3/library/functools.html#functools.total_ordering> to simplify this portion, reducing the number of functions you'll need to write.

We will not discuss class decorators in detail as their implementation is significantly more complex than function decorators. They are exactly what you might guess: functions that decorate classes. You do not need to know how to implement one to use them, and the example in the above documentation should give you what you need to know.



## Grading Rubric

* Up to 5 points for each problem

For each problem:
  * Up to 4 points for correctness (make all the tests pass)
  * Up to 1 point for idiomatic Python coding style



