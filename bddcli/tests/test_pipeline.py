import sys

from bddcli import Given, when, stdout, status, stderr, Application


def foo():  # pragma: no cover
    stdin = sys.stdin.read()
    if stdin == 'bad':
        print(f'error: {stdin}', file=sys.stderr)
        return 1
    elif stdin:
        print(f'input: {stdin}')


def test_basic_pipeline():
    app = Application('foo', 'bddcli.tests.test_pipeline:foo')
    with Given(app):
        assert status == 0
        assert stdout == ''
        assert stderr == ''

        when(stdin='bar')
        assert status == 0
        assert stdout == f'input: bar\n'

        when(stdin='bad')
        assert status == 1
        assert stderr == f'error: bad\n'

