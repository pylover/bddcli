# bddcli
Test any command line interface in BDD manner.

[![PyPI](http://img.shields.io/pypi/v/bddcli.svg)](https://pypi.python.org/pypi/bddcli)
[![Build Status](https://travis-ci.org/pylover/bddcli.svg?branch=master)](https://travis-ci.org/pylover/bddcli)
[![Coverage Status](https://coveralls.io/repos/github/pylover/bddcli/badge.svg?branch=master)](https://coveralls.io/github/pylover/bddcli?branch=master)

### About

A framework to easily test your command line interface in another(isolated) 
process and gather stdout, stderr and returnStatus of the process.

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

    when('Without any argument', given - 'bar')
    assert stdout == 'foo\n'

    when('Pass multiple arguments', 'bar baz')
    assert stdout == 'foo bar baz\n'

    when('Pass multiple arguments, another method', ['bar', 'baz'])
    assert stdout == 'foo bar baz\n'

    when('Add an argument', given + 'baz')
    assert stdout == 'foo bar baz\n'

```


### Standard input

```python
with Given(app, stdin='foo'):
    assert ...

    when('stdin is empty', stdin='')
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

    when('Without any variable', environ=given - 'bar')
    assert stdout == '\n'

    when('Add another variables', environ=given + {'qux': 'quux'})
    assert stdout == 'bar: baz qux: quux\n'
```


See tests for more examples.

