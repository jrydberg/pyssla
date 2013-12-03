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

"""Scope analyser."""

import ast

from . import ast_helpers


class ScopeAnalyser(ast.NodeVisitor):
    """Analyser of scopes."""

    def __init__(self):
        self.scopes = ScopeStack()

    def analyse(self, node):
        self.visit(node)

    def _bind(self, name, binding):
        self.scopes.top().put(name, binding)

    def _handle_load(self, node):
        name = _node_name(node)
        if not name:
            return
        binding = self.scopes.top().get(name)
        if binding:
            binding.use(self.scopes.top(), node)
            return

        scopes = [scope for scope in list(self.scopes)[:-1]
                  if isinstance(scope, (FunctionScope, ModuleScope))]
        for scope in reversed(scopes):
            binding = scope.get(name)
            if binding:
                binding.use(self.scopes.top(), node)
                return

        # ignore errors

    def _handle_store(self, node):
        name = _node_name(node)
        if not name:
            return
        # FIXME: should we keep track of all assignments?
        self._bind(name, Assignment(node))

    def _handle_del(self, node):
        name = _node_name(node)
        if not name:
            return
        if name in self.scopes.top():
            self.scopes.top().remove(name)

    def visit_Name(self, node):
        if isinstance(node.ctx, (ast.Load, ast.AugLoad)):
            self._handle_load(node)
        elif isinstance(node.ctx, (ast.Store, ast.AugStore)):
            self._handle_store(node)
        elif isinstance(node.ctx, ast.Del):
            self._handle_del(node)

    def visit_GeneratorExp(self, node):
        self.scopes.push(GeneratorScope)
        for gen in node.generators:
            self.visit(gen)
        self.visit(node.elt)
        self.scopes.pop()

    def visit_FunctionDef(self, node):
        self._bind(node.name, FunctionDefinition(node))
        self.visit_Lambda(node)
        
    def visit_Lambda(self, node):
        args = ast_helpers.collect_args(node)
        for wildcard in (node.args.vararg, node.args.kwarg):
            if not wildcard:
                continue
            args.append(wildcard)
        node.scope = self.scopes.push(FunctionScope)
        for name in args:
            self._bind(name, Argument(node))
        self.generic_visit(node)
        self.scopes.pop()

    def visit_ClassDef(self, node):
        node.scope = self.scopes.push(ClassScope)
        self.generic_visit(node)
        self.scopes.pop()
        self._bind(node.name, ClassDefinition(node))

    def visit_Module(self, node):
        node.scope = self.scopes.push(ModuleScope)
        self.generic_visit(node)
        self.scopes.pop()

    def visit_ImportFrom(self, node):
        for alias in node.names:
            self._bind(alias.asname or alias.name, Importation(
                    node, node.module))

    def visit_Import(self, node):
        for alias in node.names:
            self._bind(alias.asname or alias.name, Importation(
                    node, alias.name))


class Scope(dict):

    def put(self, name, binding):
        self[name] = binding


class FunctionScope(Scope):
    pass


class ClassScope(Scope):
    pass


class ModuleScope(Scope):
    pass


class GeneratorScope(Scope):
    pass


class Binding(object):

    def __init__(self, source):
        self.source = source
        self.uses = []

    def use(self, scope, node):
        self.uses.append((scope, node))


class Importation(Binding):

    def __init__(self, source, name):
        Binding.__init__(self, source)
        self.name = name


class Argument(Binding):
    pass


class Assignment(Binding):
    pass


class Definition(Binding):
    pass


class FunctionDefinition(Definition):
    pass


class ClassDefinition(Definition):
    pass


class ScopeStack(object):
    
    def __init__(self):
        self.scopes = []

    def __iter__(self):
        return iter(self.scopes)

    def push(self, scope_class):
        scope = scope_class()
        self.scopes.append(scope)
        return scope
    
    def pop(self):
        return self.scopes.pop()

    def top(self):
        return self.scopes[-1]


def _node_name(node):
    if hasattr(node, 'id'):
        return node.id
    if hasattr(node, 'name'):
        return node.name
    return None
