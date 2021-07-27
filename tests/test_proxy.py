import sys

from bddcli import Given, stdout, Application


def foo():  # pragma: no cover
    print(' '.join(sys.argv))


app = Application('foo', 'tests.test_proxy:foo')


def test_proxy():
    with Given(app, ['bar']):
        assert stdout == 'foo bar\n'
        assert len(stdout) == 8

        assert stdout[:-1] == 'foo bar'
