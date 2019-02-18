import sys

import pytest

from bddcli import Command, when, stdout, status, stderr, Application


def foo():
    print(' '.join(sys.argv))


def test_arguments():
    app = Application('foo', 'bddcli.tests.test_arguments:foo')
    with Command(app, 'Wihtout any arguments'):
        assert stdout == 'foo\n'

