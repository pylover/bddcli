import os
import sys
import subprocess as sp


if os.name == 'nt':
    BOOTSTRAPPER_FILENAME = 'bddcli-bootstrapper.exe'
    VENV_BINDIR = 'Scripts'

    # On Windows, os module can't kill processes by group
    # Kill all children indiscriminately instead
    def killpg_by_pid(pid, s):
        # FIXME: use s here
        sp.call(['taskkill', '/T', '/F', '/PID', str(pid)])

else:
    BOOTSTRAPPER_FILENAME = 'bddcli-bootstrapper'
    VENV_BINDIR = 'bin'

    def killpg_by_pid(pid, s):
        os.killpg(os.getpgid(pid), s)


# Find bootstrapper location
if 'VIRTUAL_ENV' in os.environ:  # pragma: no cover
    BOOTSTRAPPER_PATH = os.path.join(os.environ['VIRTUAL_ENV'], VENV_BINDIR)
    try_ = os.path.join(BOOTSTRAPPER_PATH, BOOTSTRAPPER_FILENAME)
    if not os.path.exists(try_):
        BOOTSTRAPPER_PATH = os.path.join(os.environ['HOME'], '.local', 'bin')
else:
    for d in sys.path:
        if os.path.isfile(d):
            d = os.path.dirname(d)
        try:
            if BOOTSTRAPPER_FILENAME in os.listdir(d):
                BOOTSTRAPPER_PATH = d
                break
        except (FileNotFoundError, NotADirectoryError):
            # Nothing guarantees a PATH entry is valid
            continue

    else:  # pragma: no cover
        raise FileNotFoundError(
            f'Cannot find {BOOTSTRAPPER_FILENAME} in your PATH '
            f'environment variable: {sys.path}'
        )

BOOTSTRAPPER_FULLPATH = os.path.join(BOOTSTRAPPER_PATH, BOOTSTRAPPER_FILENAME)


def Popen(command, env=None, **kw):
    if os.name == "nt":
        # On Windows, the specified env must include a valid SystemRoot
        # Use a current value
        if env is None:
            env = {}

        env["SystemRoot"] = os.environ["SystemRoot"]
        kw['creationflags'] = sp.CREATE_NEW_PROCESS_GROUP
    else:
        kw['preexec_fn'] = os.setpgrp

    return sp.Popen(command, env=env, **kw)
