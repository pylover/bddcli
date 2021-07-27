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
        assert stdout + 'baz' == 'foo bar\nbaz'
        assert stdout * 2 == 'foo bar\nfoo bar\n'
