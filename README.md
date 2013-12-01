Pyssla is a rule-based source code analyzer for Python.

Pyssla should be seen as a complement to `pyflakes` rather than a
replacement.

# Install

Install it from PyPi:

    $ pip install pyssla

# Usage

Run `pyssla` against your python files:

    $ pyssla *.py
    ast_helpers.py: 18: function is too cyclomatic complex: 16

