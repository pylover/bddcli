import sys

import pytest

from bddcli import Command, when, stdout, status, stderr, Application, given


def foo():
    print(' '.join(sys.argv))


app = Application('foo', 'bddcli.tests.test_arguments:foo')


def test_positionals():
    with Command(app, 'Pass single positional argument', positionals=['bar']):
        assert stdout == 'foo bar\n'

        when('Without any argument', positionals=given - 'bar')
        assert stdout == 'foo\n'

        when('Pass multiple arguments', positionals=given + 'baz')
        assert stdout == 'foo bar baz\n'


def test_flags():
    with Command(
        app,
        'Pass single optional argument',
        flags=['--bar=baz']
    ):
        assert stdout == 'foo --bar=baz\n'

