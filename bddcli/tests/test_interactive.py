import sys
import time

from bddcli import Given, stdout, status, Application, when


def foo():  # pragma: no cover
    print(sys.stdin.read(), flush=True)


app = Application('foo', 'bddcli.tests.test_interactive:foo')


def test_signal():
    with Given(app, nowait=True) as s:
        # Wait some moments
        time.sleep(1)
        s.wait('bar')
        assert stdout == 'bar\n'
        assert status == 0

        when(stdin='baz')
        s.wait()
        assert stdout == 'baz\n'
        assert status == 0

