import os
import sys

import pytest

from bddcli import Given, when, stdout, Application, given, stderr


def baz():  # pragma: no cover
    e = os.environ.copy()
    # For Linux and Windows
    discarded_variables = ['LC_CTYPE', 'PWD',
                           'COMSPEC', 'PATHEXT', 'PROMPT', 'SYSTEMROOT']
    # Windows environment variables are case-insensitive, lowercase them
    print(' '.join(
        f'{k}: {v}' for k, v in e.items() if k not in discarded_variables
    ).lower())
    print(' '.join(sys.argv), file=sys.stderr)


app = Application('foo', 'tests.test_manipulators:baz')


def test_dict_manipulators():
    with Given(app, environ={'bar': 'baz'}):
        assert stdout == 'bar: baz\n'

        with pytest.raises(ValueError):
            when(environ=given + {'bar': 'qux'})


def test_list_manipulators():
    with Given(app, ['bar']):
        assert stderr == 'foo bar\n'

        with pytest.raises(ValueError):
            when(given + {'invalid': 'qux'})

        with pytest.raises(ValueError):
            when(given | {'bar': 'qux'})

        when(given - 'bar')
        assert stderr == 'foo\n'

        with pytest.raises(ValueError):
            when(given - 'missing')

        when(given + ['baz', 'qux', 'quux'])
        assert stderr == 'foo bar baz qux quux\n'

        when(given - ['bar'])
        assert stderr == 'foo\n'

        class InvalidType:
            pass

        with pytest.raises(TypeError):
            when(given - InvalidType())

        with pytest.raises(TypeError):
            when(given | InvalidType())
