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
from collections import defaultdict


class Checker(ast.NodeVisitor):

    def __init__(self, filename):
        self.filename = filename
        self.messages = []
        self._rules = defaultdict(list)

    def add_rule(self, rule):
        for type in rule.types:
            self._rules[type].append(rule)

    def analyse(self, tree):
        self.visit(tree)

    def visit(self, node):
        type = node.__class__
        for rule in self._rules.get(type, []):
            rule.analyse(node, self)
        self.generic_visit(node)

    def report(self, node, message):
        self.messages.append('{0}: {1}: {2}'.format(
            self.filename, node.lineno, message))
