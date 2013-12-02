# Copyright 2013 Johan Rydberg.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import ast
import itertools

from ..rule import Rule
from .. import ast_helpers
from .. import pat


class OneImportPerLineRule(Rule):
    """Importing just a single name per import statement will make
    your code easier to read.
    """

    types = (ast.Import, ast.ImportFrom)

    defaults = {
        "enabled": False
        }

    def analyse(self, node, checker):
        if len(node.names) != 1:
            checker.report(node, "more than one name imported")


class ExcessiveImportedNamesRule(Rule):
    """If importing many names from a module it is better to import
    the module itself and refer to attributes in it.

    Example:

        # it is better to import "foo" and refer to .a, .b, and .c.
        from foo import a
        from foo import b
        from foo import c

    """
    types = (ast.Module,)

    defaults = {
        'threshold': 3
        }
    
    def _init_config(self, config):
        self.threshold = config['threshold']

    def analyse(self, node, checker):
        keyfunc = lambda node: node.module
        imports = ast_helpers.ast_path(node, './ImportFrom')
        imports.sort(key=keyfunc)
        for module, imports in itertools.groupby(imports, keyfunc):
            num_names = sum([len(child.names) for child in imports])
            if num_names >= self.threshold:
                checker.report(
                    child, "excessive name importing from module '{}'".format(
                        module))


class NeverImportWildcardRule(Rule):
    """Wildcard imports lead to namespace pollution. Things get in
    your local namespace that you didn't expect to get. You may see
    imported names obscuring module-defined local names. You won't be
    able to figure out where certain names come from.

    Although a convenient shortcut, this should not be in production
    code.
    """

    types = (ast.ImportFrom,)

    def analyse(self, node, checker):
        for alias in node.names:
            if alias.name == '*':
                checker.report(node, "never import '*'")


class UseIsinstanceRule(Rule):
    """To check whether a function parameter is of a certain type,
    don't use something like `arg.__class__ == MyClass`, use
    `isinstance(arg, MyClass)`.
    """

    types = (ast.FunctionDef,)
    
    def _init_config(self, config):
        self.pat = pat.parse('_.__class__ == _')

    def analyse(self, node, checker):
        match = pat.scan(node, self.pat)
        if match:
            checker.report(
                match, "use isinstance() instead of comparing to __class___")


class UseInDictNotInDictKeys(Rule):
    """Use `k in d` rather than `k in d.keys()` for dicts."""

    types = (ast.FunctionDef,)
    
    def _init_config(self, config):
        self.in_keys_pat = pat.parse('_ in _.keys()')
        self.has_key_pat = pat.parse('_.has_key(_)')

    def analyse(self, node, checker):
        match = pat.scan(node, self.in_keys_pat)
        if match:
            checker.report(
                match, "use 'k in d' rather than 'k in d.keys()'")
        match = pat.scan(node, self.has_key_pat)
        if match:
            checker.report(
                match, "use 'k in d' rather than 'd.has_key(k)'")


class IdiomaticModuleStructureRule(Rule):
    """Make sure that the module follow a some-what idiomatic structure."""

    types = (ast.Module,)
    order = [
        'module docstring',
        'import',
        'constant',
        'exception class',
        'interface function',
        'class',
        'internal function or class'
        ]

    def analyse(self, node, checker):
        step = 0
        for child in ast.iter_child_nodes(node):
            cls = self._classify(child)
            if cls == 'unknown':
                continue
            index = self.order.index(cls)
            if index == step:
                pass
            elif index > step:
                step = index
            elif index < step:
                before = self.order[index + 1:]
                after = self.order[:index]
                if before and after:
                    checker.report(
                        child, '{0} should come before {1} and after {2}'.format(
                            cls, ', '.join(before), ', '.join(after)))
                elif before:
                    checker.report(child, '%s should come last in module' % cls)
                elif after:
                    checker.report(child, '%s should come first in module' % cls)

    def _classify(self, child):
        if isinstance(child, ast.Str):
            return 'module docstring'
        elif (isinstance(child, ast.Import) or
              isinstance(child, ast.ImportFrom)):
            return 'import'
        elif isinstance(child, ast.Assign):
            # allow internal constants everywhere
            if (isinstance(child.targets[0], ast.Name) and
                child.targets[0].id.startswith('_')):
                return 'unknown'
            return 'constant'
        elif isinstance(child, ast.ClassDef):
            if child.name.startswith("_"):
                return 'internal function or class'
            elif child.name.endswith("Error"):
                return 'exception class'
            else:
                return 'class'
        elif isinstance(child, ast.FunctionDef):
            if child.name.startswith("_"):
                return 'internal function or class'
            else:
                return 'interface function'
        else:
            return 'unknown'
