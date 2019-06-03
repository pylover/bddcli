import sys

from bddcli import Given, when, stdout, status, stderr, Application


def foo():  # pragma: no cover
    stdin = sys.stdin.buffer.read()
    sys.stdout.buffer.write(stdin)


def test_binary_pipeline():
    app = Application('foo', 'bddcli.tests.test_pipeline_binary:foo')
    with Given(app, stdin=b'bar'):
        assert stderr == b''
        assert stdout == b'bar'
        assert status == 0



