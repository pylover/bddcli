import sys

import pytest

from bddcli import Command, when, stdout, status, stderr, Application, given


def foo():
    print(' '.join(sys.argv))


def test_arguments():
    app = Application('foo', 'bddcli.tests.test_arguments:foo')
    with Command(app, 'Pass a single argument', positionals=['bar']):
        assert stdout == 'foo bar\n'

        when('Without any argument', positionals=given - 'bar')
        assert stdout == 'foo\n'

        when('Pass multiple arguments', positionals=given + 'baz')
        assert stdout == 'foo bar baz\n'


