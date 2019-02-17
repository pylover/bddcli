import sys

import pytest

from bddcli import Command, when, stdout, status, stderr, Application


def foo():
    stdin = sys.stdin.read()
    if stdin == 'bad':
        print('Bad', file=sys.stderr)
        return 1

    print('Foo')
    return 0


def test_stdin():
    app = Application('foo', 'bddcli.tests.test_stdin:foo')
    with Command(app, 'Wihtout any parameter'):
        assert stderr == ''
        assert status == 0
        assert stdout == 'Foo\n'

        when('Standart input is bad', stdin='bad')
        assert status == 1
        assert stderr == 'Bad\n'
        assert stdout == ''

