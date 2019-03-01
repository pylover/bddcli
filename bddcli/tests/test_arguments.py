import sys

import pytest

from bddcli import Given, given, when, stdout, status, stderr, Application


def foo():  # pragma: no cover
    print(' '.join(sys.argv))


app = Application('foo', 'bddcli.tests.test_arguments:foo')


def test_arguments():
    with Given(app, arguments=['bar']):
        assert stdout == 'foo bar\n'

        when(arguments=given - 'bar')
        assert stdout == 'foo\n'

        when(arguments=given + 'baz')
        assert stdout == 'foo bar baz\n'

