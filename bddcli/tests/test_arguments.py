import sys

import pytest

from bddcli import Command, when, stdout, status, stderr, Application, given


def foo():  # pragma: no cover
    print(' '.join(sys.argv))


app = Application('foo', 'bddcli.tests.test_arguments:foo')


def test_arguments():
    with Command(app, arguments=['bar']):
        assert stdout == 'foo bar\n'

        when(arguments=given - 'bar')
        assert stdout == 'foo\n'

        when(arguments=given + 'baz')
        assert stdout == 'foo bar baz\n'

