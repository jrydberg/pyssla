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

from ..rule import Rule
from .. import ast_helpers


class ExcessivePublicMethodsRule(Rule):
    """Classes with large numbers of public methods and attributes
    require disproportionate testing efforts since combinational side
    effects grow rapidly and increase risk. Refactoring these classes
    into smaller ones not only increases testability and reliability
    but also allows new variations to be developed easily.
    """
    types = (ast.ClassDef,)

    defaults = {
        'threshold': 20
        }
    
    def _init_config(self, config):
        self.threshold = config.get('threshold', 20)

    def analyse(self, node, checker):
        fns = [stmt for stmt in node.body
               if isinstance(stmt, ast.FunctionDef)
               and stmt.name[0] != '_']
        if len(fns) >= self.threshold:
            checker.report(
                node, "excessive number of public methods: {0}".format(
                    len(fns)))


class ExcessiveArgumentListRule(Rule):
    """Methods with numerous parameters are a challenge to
    maintain. These situations usually denote the need for new objects
    to wrap the numerous parameters.
    """

    types = (ast.FunctionDef,)

    defaults = {
        'threshold': 10
        }
    
    def _init_config(self, config):
        self.threshold = config.get('threshold', 10)

    def analyse(self, node, checker):
        args = ast_helpers.collect_args(node)
        if len(args) >= self.threshold:
            checker.report(
                node, "excessive argument list: {0} args".format(
                    len(args)))


class _ExcessiveRule(Rule, ast.NodeVisitor):

    def visit(self, node):
        if hasattr(node, "lineno"):
            if not self.first:
                self.first = node.lineno
            self.last = max(self.last, node.lineno)
        self.generic_visit(node)

    def analyse(self, node, checker):
        self.first = self.last = 0
        self.generic_visit(node)
        return self.last - self.first
        if linecnt >= self.threshold:
            checker.report(
                node, "excessive function length: {0} lines".format(linecnt))


class ExcessiveFunctionLengthRule(_ExcessiveRule):
    """When methods are excessively long this usually indicates that
    the method is doing more than its name/signature might
    suggest. They also become challenging for others to digest since
    excessive scrolling causes readers to lose focus.

    Try to reduce the method length by creating helper methods and
    removing any copy/pasted code.
    """
    types = (ast.FunctionDef,)

    defaults = {
        'threshold': 50
        }

    def _init_config(self, config):
        self.threshold = config.get('threshold', 50)

    def analyse(self, node, checker):
        linecnt = _ExcessiveRule.analyse(self, node, checker)
        if linecnt >= self.threshold:
            checker.report(
                node, "excessive function length: {0} lines".format(linecnt))


class ExcessiveClassLengthRule(_ExcessiveRule):
    """Excessive class lengths are usually indications that the class
    may be burdened with excessive responsibilities that could be
    provided by external classes or functions. In breaking these
    methods apart the code becomes more managable and ripe for reuse.
    """
    types = (ast.ClassDef,)

    defaults = {
        'threshold': 200
        }

    def _init_config(self, config):
        self.threshold = config.get('threshold', 200)

    def analyse(self, node, checker):
        linecnt = _ExcessiveRule.analyse(self, node, checker)
        if linecnt >= self.threshold:
            checker.report(
                node, "excessive class length: {0} lines".format(linecnt))


class TooManyFieldsRule(Rule):
    """Classes that have too many fields can become unwieldy and could
    be redesigned to have fewer fields, possibly through grouping
    related fields in new objects.

    For example, a class with individual city/state/zip fields could
    park them within a single Address field.
    """
    types = (ast.ClassDef,)

    defaults = {
        'threshold': 15
        }

    path = (
        "./FunctionDef[name=='__init__']"
        "//Assign/Attribute[value.id=='self' and isinstance(ctx, ast.Store)]"
        )

    def _init_config(self, config):
        self.threshold = config.get('threshold', 15)

    def analyse(self, node, checker):
        c = len(ast_helpers.ast_path(node, self.path))
        if c >= self.threshold:
            checker.report(
                node, "too many fields: {0}".format(c))


class TooManyMethods(Rule):
    """A class with too many methods is probably a good suspect for
    refactoring, in order to reduce its complexity and find a way to
    have more fine grained objects.
    """

    types = (ast.ClassDef,)

    defaults = {
        'threshold': 10
        }

    def _init_config(self, config):
        self.threshold = config.get('threshold', 10)

    def analyse(self, node, checker):
        c = len(ast_helpers.ast_path(node, "./FunctionDef"))
        if c >= self.threshold:
            checker.report(node, "too many methods: {0}".format(c))
