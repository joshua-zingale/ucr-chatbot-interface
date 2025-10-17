# Contributing

This project uses [uv](https://docs.astral.sh/uv/) for managing the Python dependencies.
You must use `uv` as well.

## Code Linting

The following tools are used to maintain code quality:
- All code must pass [pyright](https://github.com/microsoft/pyright) on "standard" mode,
which checks for code correctness via type hints in the Python code.
- The configured [Ruff](https://docs.astral.sh/ruff/) checks must pass, which
  check for styling and common errors.

To run the checks with `uv`, navigate to the root directory of this project
and run
```bash
uv run pyright # Check types
uv run ruff check # Check common errors
uv run ruff format --check # Check formatting
```

Run these should always be passing before you push code.

## Type Hints
Python has optional [type hints](https://www.geeksforgeeks.org/python/type-hints-in-python/) that help other humans and code checkers understand your code.
For this project, they are not optional but must be used.

All functions and methods must have their parameters' types stated explicitly
via type hints. Also, the return values must be explicitly typed or inferable
by [pyright](https://github.com/microsoft/pyright). For example,

```python
def add(a, b):
    return a + b
```

is not okay but

```python
def add(a: int, b: int):
    return a + b
```

or

```python
def add(a: int, b: int) -> int:
    return a + b
```

is okay. Explicitly stating the output type when convenient is preferred.

## Doc Strings

Every class, method, and function must have docstring attached to it
that explains the purpose of the class and functionality of the method/function.

## Formatting

To format your code, simply run

```bash
uv run ruff format
```

from the root directory. This will fix the spacing, quote usage, and other
aesthetic features of your code.
After running this, your code will pass ruff's format check.
