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

from .checker import Checker


def process(config, filename, exts):
    with open(filename) as filep:
        tree = ast.parse(filep.read(), filename)

    checker = Checker(filename)
    for ext in exts:
        checker.add_rule(ext.plugin(
            config.get(ext.name, {})))

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
