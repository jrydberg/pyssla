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


class ShortVariableRule(Rule):
    """Variables that are very short are not helpful to the reader.
    """

    types = (ast.FunctionDef,)
    
    def _init_config(self, config):
        self.threshold = config.get('threshold', 3)

    def analyse(self, node, checker):
        names = ast_helpers.ast_path(node, './/Name[isinstance(ctx, ast.Store)]')
        for name in names:
            if len(name.id) < self.threshold:
                checker.report(name, "too short variable name")
