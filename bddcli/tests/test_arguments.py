import sys

import pytest

from bddcli import Command, when, stdout, status, stderr, Application


def foo():
    print(' '.join(sys.argv))


def test_arguments():
    app = Application('foo', 'bddcli.tests.test_arguments:foo')
    with Command(app, 'Wihtout any arguments'):
        assert stdout == 'foo\n'

        when('Pass a single argument', positionals=['bar'])
        assert stdout == 'foo bar\n'

        when('Pass multiple arguments', positionals=['bar', 'baz'])
        assert stdout == 'foo bar baz\n'

