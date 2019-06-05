import sys

import pytest

from bddcli import Given, given, when, stdout, status, stderr, Application


def foo():  # pragma: no cover
    print(' '.join(sys.argv))


app = Application('foo', 'bddcli.tests.test_arguments:foo')


def test_arguments():
    with Given(app, ['bar']):
        assert stdout == 'foo bar\n'
        assert status == 0

        when(given - 'bar')
        assert stdout == 'foo\n'

        when(given + 'baz')
        assert stdout == 'foo bar baz\n'

    with Given(app, 'bar'):
        assert stdout == 'foo bar\n'

        when('baz')
        assert stdout == 'foo baz\n'

    # Given without arguments
    with Given(app):

        # Then, when with the given
        when(given + 'qux')
        assert stdout == 'foo qux\n'
