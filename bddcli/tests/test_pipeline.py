import sys

import pytest

from bddcli import Command, when, stdout, status, stderr


def test_basic_pipeline():
    def f():
        print('Foo')
        print('Bar', file=sys.stderr)
        return 0

    with Command(f, 'Wihtour parameters'):
        assert status == 0
        assert stdout == 'Foo\n'
        assert stderr == 'Bar\n'

