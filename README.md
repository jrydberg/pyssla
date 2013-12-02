Pyssla is a rule-based source code analyzer for Python.

# Introduction

TL;DR: Pyssla will check if your Python code is decent shape.

Pyssla will analyse Python code and see if it conforms to a set of
rules.  There are rules for all kinds of different things ranging from
naming of local variables to cyclomatic complexity.  

For a complete list of rules, see [RULES.md](RULES.md).

# Install

Install it from PyPi:

    $ pip install pyssla

# Usage

Run `pyssla` against your python files:

    $ pyssla ../pyflakes/pyflakes/*.py
    ../pyflakes/pyflakes/api.py: 59: too short variable name
    ../pyflakes/pyflakes/api.py: 62: too short variable name
    ../pyflakes/pyflakes/api.py: 81: too short variable name
    ../pyflakes/pyflakes/api.py: 129: too short variable name
    ../pyflakes/pyflakes/checker.py: 208: interface function should come before class, internal function or class and after module docstring, import, constant, exception class
    ../pyflakes/pyflakes/checker.py: 216: too many methods: 43
    ../pyflakes/pyflakes/checker.py: 216: excessive number of public methods: 42
    ../pyflakes/pyflakes/checker.py: 216: excessive class length: 643 lines
    ../pyflakes/pyflakes/checker.py: 368: too short variable name
    ../pyflakes/pyflakes/checker.py: 394: function is too cyclomatic complex: 17
    ../pyflakes/pyflakes/checker.py: 442: function is too cyclomatic complex: 14
    ../pyflakes/pyflakes/checker.py: 481: function is too cyclomatic complex: 14
    ../pyflakes/pyflakes/checker.py: 586: too short variable name
    ../pyflakes/pyflakes/checker.py: 672: too short variable name
    ../pyflakes/pyflakes/checker.py: 672: too short variable name
    ../pyflakes/pyflakes/checker.py: 713: excessive function length: 61 lines
    ../pyflakes/pyflakes/checker.py: 713: function is too cyclomatic complex: 16
    ../pyflakes/pyflakes/checker.py: 818: too short variable name
    ../pyflakes/pyflakes/example.py: 4: too short variable name
    ../pyflakes/pyflakes/messages.py: 68: exception class should come before interface function, class, internal function or class and after module docstring, import, constant
    ../pyflakes/pyflakes/rules.py: 14: interface function should come before class, internal function or class and after module docstring, import, constant, exception class
