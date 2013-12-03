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
import argparse
import sys

from stevedore import extension

from .analyser import ScopeAnalyser
from .checker import Checker
from . import ast_helpers


def process(config, filename, exts):
    with open(filename) as filep:
        tree = ast.parse(filep.read(), filename)

    ast_helpers.set_parent(tree)

    analyser = ScopeAnalyser()
    analyser.analyse(tree)

    checker = Checker(filename)
    for ext in exts:
        rule_conf = getattr(ext.plugin, 'defaults', {})
        rule_conf.update(config.get(ext.name, {}))
        enabled = rule_conf.get('enabled', True)
        if enabled:
            checker.add_rule(ext.plugin(rule_conf))

    checker.analyse(tree)

    return checker.messages


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'files',
        nargs='+',
        default='simple',
        help='the files to analyse'
    )
    parser.add_argument(
        '-d', '--disable',
        nargs='*',
        default=[],
        type=str,
        help='rules to disable',
    )

    parser.add_argument(
        '-c', '--config',
        type=str,
        help='pyssla config file'
        )

    parsed_args = parser.parse_args()

    config = {}

    mgr = extension.ExtensionManager(
        namespace='pyssla.rules',
        invoke_on_load=False
        )
    exts = [ext for ext in mgr
            if ext.name not in parsed_args.disable]

    messages = []

    for filename in parsed_args.files:
        messages.extend(process(config, filename, exts))

    if messages:
        for message in messages:
            print message

        sys.exit(1)
