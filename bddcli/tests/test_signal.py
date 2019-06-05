import signal
import time

from bddcli import Given, stdout, status, Application


def foo():  # pragma: no cover
    done = None

    def terminate(s, f):
        nonlocal done
        done = s
        print('Signal received:', s, flush=True)

    signal.signal(signal.SIGTERM, terminate)

    while done is None:
        time.sleep(.6)

    return done


app = Application('foo', 'bddcli.tests.test_signal:foo')


def test_signal():
    with Given(app, 'bar', nowait=True) as s:
        # Wait some moments
        time.sleep(1)
        s.kill()
        s.wait()
        assert stdout == 'Signal received: 15\n'
        assert status == -signal.SIGTERM.value

