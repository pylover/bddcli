import sys

import pytest

from bddcli import Command, when, stdout, status, stderr, Application, given


def foo():  # pragma: no cover
    print(' '.join(sys.argv))


app = Application('foo', 'bddcli.tests.test_arguments:foo')


def test_arguments():
    with Command(app, 'Pass single positional argument', arguments=['bar']):
        assert stdout == 'foo bar\n'

        when('Without any argument', arguments=given - 'bar')
        assert stdout == 'foo\n'

        when('Pass multiple arguments', arguments=given + 'baz')
        assert stdout == 'foo bar baz\n'

