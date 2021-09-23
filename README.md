# bddcli
Test any command line interface in BDD manner.

[![PyPI](http://img.shields.io/pypi/v/bddcli.svg)](https://pypi.python.org/pypi/bddcli)
[![Build](https://github.com/pylover/bddcli/workflows/Build/badge.svg?branch=master)](https://github.com/pylover/bddcli/actions)
[![Coverage Status](https://coveralls.io/repos/github/pylover/bddcli/badge.svg?branch=master)](https://coveralls.io/github/pylover/bddcli?branch=master)

### About

A framework to easily test your command line interface in another(isolated) 
process and gather `stdout`, `stderr` and `exit-status` of the process.

Thanks to https://github.com/cheremnov for the Windows support.

## Installation

Only `Python >= 3.6` is supported.

```bash
pip install bddcli
```

## Quickstart

### Arguments

```python
import sys

from bddcli import Given, when, stdout, status, stderr, Application, given


def foo():
    print(' '.join(sys.argv))
    return 0


app = Application('foo', 'mymodule:foo')


with Given(app, 'bar'):
    assert status == 0
    assert stdout == 'foo bar\n'

    # Without any argument
    when(given - 'bar')
    assert stdout == 'foo\n'

    # Pass multiple arguments
    when('bar baz')
    assert stdout == 'foo bar baz\n'

    # Pass multiple arguments, another method
    when(['bar', 'baz'])
    assert stdout == 'foo bar baz\n'

    # Add an argument
    when(given + 'baz')
    assert stdout == 'foo bar baz\n'

```


### Standard input

```python
with Given(app, stdin='foo'):
    assert ...

    # stdin is empty
    when(stdin='')
    assert ...

```


### Standard output and error

```python
from bddcli import stderr, stdout

assert stderr == ... 
assert stdout == ... 
```

### Environment variables

```python
import os

from bddcli import Given, stdout, Application, when, given


def foo():
    e = os.environ.copy()
    del e['PWD']
    print(' '.join(f'{k}: {v}' for k, v in e.items()))


app = Application('foo', 'mymodule:foo')
with Given(app, environ={'bar': 'baz'}):
    assert stdout == 'bar: baz\n'

    # Without any variable
    when(environ=given - 'bar')
    assert stdout == '\n'

    # Add another variables
    when(environ=given + {'qux': 'quux'})
    assert stdout == 'bar: baz qux: quux\n'
```


See tests for more examples.

