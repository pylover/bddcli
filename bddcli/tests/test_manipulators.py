import os
import sys

import pytest

from bddcli import Command, when, stdout, Application, given


def baz():
    e = os.environ.copy()
    del e['PWD']
    print(' '.join(f'{k}: {v}' for k, v in e.items()))


app = Application('foo', 'bddcli.tests.test_manipulators:baz')


def test_manipulators():
    with Command(app, 'Test manipulators', environ={'bar': 'baz'}):
        assert stdout == 'bar: baz\n'

        with pytest.raises(ValueError):
            when('Without any argument', environ=given + {'bar': 'qux'})

