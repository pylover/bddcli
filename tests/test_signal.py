import os
import signal
import time

from bddcli import Given, stdout, status, Application, when


def foo():  # pragma: no cover
    done = None

    def terminate(s, f):
        nonlocal done
        done = s
        print('Signal received:', s, flush=True)

    if os.name == "posix":
        signal.signal(signal.SIGTERM, terminate)
        signal.signal(signal.SIGINT, terminate)

    # Prevent hanging in a case of failure
    ticks = 0
    while done is None and ticks < 50:
        time.sleep(.6)
        ticks += 1

    if ticks >= 50:
        print("Timeout")

    return done


app = Application('foo', 'tests.test_signal:foo')


def test_signal():
    with Given(app, nowait=True) as s:
        # Wait some moments
        if os.name == "nt":
            # Windows doesn't support the Unix signals.
            # Simply check if the process didn't timeout.
            time.sleep(1)
            s.kill()
            s.wait()
            assert stdout == ''
        else:
            time.sleep(1)
            s.kill()
            s.wait()
            assert stdout == 'Signal received: 15\n'
            assert status == -15

            when()
            time.sleep(1)
            s.kill(signal.SIGINT)
            s.wait()
            assert stdout == 'Signal received: 2\n'
            assert status == -2
