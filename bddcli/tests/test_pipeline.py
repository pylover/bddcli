import sys

from bddcli import Command, when, stdout, status, stderr, Application


def foo():
    stdin = sys.stdin.read()
    if stdin == 'bad':
        print(f'error: {stdin}', file=sys.stderr)
        return 1
    elif stdin:
        print(f'input: {stdin}')


def test_basic_pipeline():
    app = Application('foo', 'bddcli.tests.test_pipeline:foo')
    with Command(app, 'Wihtout any parameter and event any pipe.'):
        assert status == 0
        assert stdout == ''
        assert stderr == ''

        when('stdin is given', stdin='bar')
        assert status == 0
        assert stdout == f'input: bar\n'

        when('Exit status is not zero', stdin='bad')
        assert status == 1
        assert stderr == f'error: bad\n'

