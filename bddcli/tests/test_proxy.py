import sys

import pytest

from bddcli import Given, given, when, stdout, status, stderr, Application


def foo():  # pragma: no cover
    print(' '.join(sys.argv))


app = Application('foo', 'bddcli.tests.test_proxy:foo')


def test_proxy():
    with Given(app, ['bar']):
        assert stdout == 'foo bar\n'
        assert len(stdout) == 8

