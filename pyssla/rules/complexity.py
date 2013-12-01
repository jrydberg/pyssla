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


class _CyclomaticVisitor(ast.NodeVisitor):
    complexity = 0

    def visit(self, node):
        cls = node.__class__
        if cls in (ast.TryExcept,):
            self.complexity += len(node.handlers) + len(node.orelse)
        elif cls in (ast.BoolOp,):
            self.complexity += len(node.values) - 1
        elif cls in (ast.Lambda, ast.With, ast.If, ast.IfExp, ast.Assert):
            self.complexity += 1
        elif cls in (ast.For, ast.While):
            self.complexity += 1 + len(node.orelse) 
        ast.NodeVisitor.generic_visit(self, node)


class CyclomaticComplexityRule(Rule):
    """Complexity directly affects maintenance costs is determined by
    the number of decision points in a method plus one for the method
    entry.  The decision points include 'if', 'while', 'for', and
    'case labels' calls.

    Generally, numbers ranging from 1-4 denote low complexity, 5-7
    denote moderate complexity, 8-10 denote high complexity, and 11+
    is very high complexity.
    """
    types = (ast.FunctionDef,)

    def _init_config(self, config):
        self.threshold = config.get('threshold', 10)

    def analyse(self, node, checker):
        cv = _CyclomaticVisitor()
        cv.visit(node)
        if cv.complexity >= self.threshold:
            checker.report(
                node, "function is too cyclomatic complex: {0}".format(
                    cv.complexity))

