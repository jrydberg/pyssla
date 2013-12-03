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


class ChangingNameInClosureRule(Rule):
    """Using variables in a closure that has been defined in a loop
    normally leads to unexpected and buggy behavior

    Example:

        for name in ('a', 'b'):
            def cb():
                return "wow! {0}".format(name)
            add_callback(cb)
    """

    types = (ast.FunctionDef,)

    def analyse(self, node, checker):
        closures = ast_helpers.ast_path(node, './/FunctionDef')
        for closure in closures:
            names = ast_helpers.ast_path(
                closure, './/Name[isinstance(ctx, ast.Load)]')
            for name in names:
                if name.id in closure.scope:
                    continue
                # walk upwards the tree until we find the scope
                # where the name was defined.  keep track if
                # we have seen a loop along the way.
                source = closure
                seen_loop = False
                while source is not None:
                    if hasattr(source, 'scope'):
                        if name.id in source.scope:
                            break
                        seen_loop = False
                    if isinstance(source, (ast.For, ast.While)):
                        seen_loop = True
                    source = source.parent
                if source and seen_loop:
                    checker.report(
                        name, "using possibly changing name '{}' in a closure".format(
                            name.id))
