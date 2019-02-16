import pytest

from bddcli import Command, when, stdout


def test_basic_pipeline():
    def f():
        print('Fancy')

    with Command(f, 'Wihtour parameters'):
        assert stdout == 'Fancy\n'

