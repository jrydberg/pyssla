# short-variable #

Variables that are very short are not helpful to the reader.

Parameter | Default Value
--- | ---
threshold | 3

**Implementation**: `pyssla.rules.naming:ShortVariableRule`

# too-many-methods #

A class with too many methods is probably a good suspect for
refactoring, in order to reduce its complexity and find a way to
have more fine grained objects.

Parameter | Default Value
--- | ---
threshold | 10

**Implementation**: `pyssla.rules.code_size:TooManyMethods`

# never-import-wildcard #

Wildcard imports lead to namespace pollution. Things get in
your local namespace that you didn't expect to get. You may see
imported names obscuring module-defined local names. You won't be
able to figure out where certain names come from.

Although a convenient shortcut, this should not be in production
code.

**Implementation**: `pyssla.rules.basic:NeverImportWildcardRule`

# excessive-public-methods #

Classes with large numbers of public methods and attributes
require disproportionate testing efforts since combinational side
effects grow rapidly and increase risk. Refactoring these classes
into smaller ones not only increases testability and reliability
but also allows new variations to be developed easily.

Parameter | Default Value
--- | ---
threshold | 20

**Implementation**: `pyssla.rules.code_size:ExcessivePublicMethodsRule`

# excessive-argument-list #

Methods with numerous parameters are a challenge to
maintain. These situations usually denote the need for new objects
to wrap the numerous parameters.

Parameter | Default Value
--- | ---
threshold | 10

**Implementation**: `pyssla.rules.code_size:ExcessiveArgumentListRule`

# excessive-class-length #

Excessive class lengths are usually indications that the class
may be burdened with excessive responsibilities that could be
provided by external classes or functions. In breaking these
methods apart the code becomes more managable and ripe for reuse.

Parameter | Default Value
--- | ---
threshold | 200

**Implementation**: `pyssla.rules.code_size:ExcessiveClassLengthRule`

# use-imports-for-packages-and-modules-only #

Use imports for packages and modules only. This namespace
management convention is simple: the source of each identifier is
indicated in a consistent way; `x.obj` says that object `obj` is
defined in module `x`.

Use `import x` for importing packages and modules.  Use `from x
import y` where *x* is the package prefix and *y* is the module
name with no prefix.  Use `from x import y as z` if two modules
named *y* are to be imported or if *y* is an inconveniently long
name.

For example the module `sound.effects.echo` may be imported as
follows:

    from sound.effects import echo
    echo.EchoFilter(input, output, delay=0.7, atten=4)

Parameter | Default Value
--- | ---
enabled | False

**Implementation**: `pyssla.rules.basic:UseImportsForPackagesAndModulesOnlyRule`

# use-isinstance #

To check whether a function parameter is of a certain type,
don't use something like `arg.__class__ == MyClass`, use
`isinstance(arg, MyClass)`.

**Implementation**: `pyssla.rules.basic:UseIsinstanceRule`

# one-import-per-line #

Importing just a single name per import statement will make
your code easier to read.

Parameter | Default Value
--- | ---
enabled | False

**Implementation**: `pyssla.rules.basic:OneImportPerLineRule`

# excessive-imported-names #

If importing many names from a module it is better to import
the module itself and refer to attributes in it.

Example:

    # it is better to import "foo" and refer to .a, .b, and .c.
    from foo import a
    from foo import b
    from foo import c

Parameter | Default Value
--- | ---
threshold | 3

**Implementation**: `pyssla.rules.basic:ExcessiveImportedNamesRule`

# excessive-function-length #

When methods are excessively long this usually indicates that
the method is doing more than its name/signature might
suggest. They also become challenging for others to digest since
excessive scrolling causes readers to lose focus.

Try to reduce the method length by creating helper methods and
removing any copy/pasted code.

Parameter | Default Value
--- | ---
threshold | 50

**Implementation**: `pyssla.rules.code_size:ExcessiveFunctionLengthRule`

# changing-name-in-closure #

Using variables in a closure that has been defined in a loop
normally leads to unexpected and buggy behavior

Example:

    for name in ('a', 'b'):
        def cb():
            return "wow! {0}".format(name)
        add_callback(cb)

**Implementation**: `pyssla.rules.bugs:ChangingNameInClosureRule`

# cyclomatic-complexity #

Complexity directly affects maintenance costs is determined by
the number of decision points in a method plus one for the method
entry.  The decision points include `if`, `while`, `for`, lambdas,
`with`, `assert`, `try` and bool operations.

Generally, numbers ranging from 1-4 denote low complexity, 5-7
denote moderate complexity, 8-10 denote high complexity, and 11+
is very high complexity.

Parameter | Default Value
--- | ---
threshold | 10

**Implementation**: `pyssla.rules.complexity:CyclomaticComplexityRule`

# too-many-fields #

Classes that have too many fields can become unwieldy and could
be redesigned to have fewer fields, possibly through grouping
related fields in new objects.

For example, a class with individual city/state/zip fields could
park them within a single Address field.

Parameter | Default Value
--- | ---
threshold | 15

**Implementation**: `pyssla.rules.code_size:TooManyFieldsRule`

# use-in-dict-not-in-dict-keys #

Use `k in d` rather than `k in d.keys()` for dicts.

**Implementation**: `pyssla.rules.basic:UseInDictNotInDictKeys`

# idiomatic-module-structure #

Make sure that the module follow a some-what idiomatic structure.

**Implementation**: `pyssla.rules.basic:IdiomaticModuleStructureRule`

