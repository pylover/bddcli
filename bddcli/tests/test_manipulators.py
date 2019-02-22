import os
import sys

import pytest

from bddcli import Command, when, stdout, Application, given, stderr


def baz():
    e = os.environ.copy()
    del e['PWD']
    print(' '.join(f'{k}: {v}' for k, v in e.items()))
    print(' '.join(sys.argv), file=sys.stderr)


app = Application('foo', 'bddcli.tests.test_manipulators:baz')


def test_dict_manipulators():
    with Command(app, 'Test dictionary manipulators', environ={'bar': 'baz'}):
        assert stdout == 'bar: baz\n'

        with pytest.raises(ValueError):
            when('Append an existing item', environ=given + {'bar': 'qux'})


def test_list_manipulators():
    with Command(app, 'Test list manipulators', positionals=['bar']):
        assert stderr == 'foo bar\n'

        with pytest.raises(ValueError):
            when('Append invalid type', positionals=given + {'invalid': 'qux'})

