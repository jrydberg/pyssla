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

from setuptools import setup, find_packages

setup(
    name="pyssla",
    version="0.1",
    packages=find_packages(),
    description="rule-based source code analyzer for Python",
    author="Johan Rydberg",
    author_email="johan.rydberg@gmail.com",
    license="Apache 2.0",
    install_requires=[
        "PyYAML",
        "stevedore"
        ],
    entry_points={
        'console_scripts': [
            'pyssla = pyssla.script:main'
            ],
        'pyssla.rules': [
            'excessive-function-length = pyssla.rules.code_size:ExcessiveFunctionLengthRule',
            'excessive-class-length = pyssla.rules.code_size:ExcessiveClassLengthRule',
            'excessive-argument-list = pyssla.rules.code_size:ExcessiveArgumentListRule',
            'excessive-public-methods = pyssla.rules.code_size:ExcessivePublicMethodsRule',
            'too-many-fields = pyssla.rules.code_size:TooManyFieldsRule',
            'too-many-methods = pyssla.rules.code_size:TooManyMethods',
            'cyclomatic-complexity = pyssla.rules.complexity:CyclomaticComplexityRule',
            'use-isinstance = pyssla.rules.basic:UseIsinstanceRule',
            'one-import-per-line = pyssla.rules.basic:OneImportPerLineRule',
            'use-imports-for-packages-and-modules-only = pyssla.rules.basic:UseImportsForPackagesAndModulesOnlyRule',
            'excessive-imported-names = pyssla.rules.basic:ExcessiveImportedNamesRule',
            'never-import-wildcard = pyssla.rules.basic:NeverImportWildcardRule',
            'idiomatic-module-structure = pyssla.rules.basic:IdiomaticModuleStructureRule',
            'use-in-dict-not-in-dict-keys = pyssla.rules.basic:UseInDictNotInDictKeys',
            'short-variable = pyssla.rules.naming:ShortVariableRule',
            'changing-name-in-closure = pyssla.rules.bugs:ChangingNameInClosureRule',
            ],
        },
    zip_safe=False
)
