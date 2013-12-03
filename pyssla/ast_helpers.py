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


def set_parent(node, parent=None):
    node.parent = parent
    for child in ast.iter_child_nodes(node):
        set_parent(child, node)


def ast_path(node, path):
    """."""
    tokens = path.split('/')
    result = [node]
    for token in tokens:
        if token == '.':
            pass
        elif token == '*':
            def select(result):
                for elem in result:
                    for celem in ast.iter_child_nodes(elem):
                        yield celem
            result = select(result)
        elif token == '':
            def select(result):
                for elem in result:
                    for celem in ast.walk(elem):
                        yield celem
            result = select(result)
        else:
            if '[' in token:
                token, rest = token.split('[', 1)
                predicate = rest[:-1]
            else:
                predicate = None

            def select(result, name):
                for elem in result:
                    for celem in ast.iter_child_nodes(elem):
                        if celem.__class__.__name__ == name:
                            yield celem
            result = select(result, token)
            result = list(result)
            if predicate:
                def select(result, predicate=predicate):
                    for elem in result:
                        vars = dict([(field, getattr(elem, field))
                                     for field in elem._fields])
                        try:
                            val = eval(predicate, globals(), vars)
                        except Exception:
                            val = False
                        if val:
                            yield elem
                result = select(result)

    return list(result)


def collect_args(node):
    args = []

    def add_args(arglist):
        for arg in arglist:
            if isinstance(arg, ast.Tuple):
                add_args(arg.elts)
            else:
                args.append(arg.id)

    assert isinstance(node, ast.FunctionDef)
    add_args(node.args.args)

    return args
