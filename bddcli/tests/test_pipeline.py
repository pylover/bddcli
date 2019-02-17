import sys

import pytest

from bddcli import Command, when, stdout, status, stderr


def foo():
    stdin = sys.stdin.read()
    if stdin == 'bad':
        print('Bad', file=sys.stderr)
        return 1

    print('Foo')
    return 0


def test_basic_pipeline():
    with Command('bddcli.tests.test_pipeline:foo', 'Wihtout any parameter'):
        assert status == 0
        assert stdout == 'Foo\n'
        assert stderr == ''

        when('Standart input is bad', stdin='bad')
        assert status == 1
        assert stderr == 'Bad\n'
        assert stdout == ''

