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

"""Simple pattern matching for AST trees."""

import ast


def match(node, pat):
    """Return `True` if AST tree `node` matches AST pattern `pat`.
    """
    if isinstance(pat, ast.Name) and pat.id == '_':
        return True
    elif isinstance(pat, ast.AST):
        if not isinstance(node, ast.AST):
            return False
        if not (issubclass(node.__class__, pat.__class__) or
                issubclass(pat.__class__, node.__class__)):
            return False
        assert _check_fields(node, pat)
        for (field1, val1), (field2, val2) in \
                zip(ast.iter_fields(node),
                    ast.iter_fields(pat)):
            assert(field1 == field2)
            if not match(val1, val2):
                return False
    elif isinstance(pat, list):
        if not isinstance(node, list):
            return False
        if len(node) != len(pat):
            return False
        for val1, val2 in zip(node, pat):
            if not match(val1, val2):
                return False
    else:
        # Primitive comparison.
        if node != pat:
            return False

    return True
                
    
def scan(node, pat):
    """."""
    if match(node, pat):
        return node
    for child in ast.walk(node):
        if match(child, pat):
            return child
    return None


def parse(s):
    node = ast.parse(s).body[0]
    if isinstance(node, ast.Expr):
        node = node.value
    return node

    
def _check_fields(node1, node2):
    """Return True if node1 and node2 have the same _fields attribute,
    and both have all of their fields present. Return False otherwise.
    """
    if node1._fields != node2._fields:
        return False
    for f in node1._fields:
        if not (hasattr(node1, f) and hasattr(node2, f)):
            return False
    return True
