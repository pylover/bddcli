''' A module for platform-dependent functions
'''
import os
import subprocess as sp


def killpg(pid, s):
    if os.name == "nt":
        # On Windows, os module can't kill processes by group
        # Kill all children indiscriminately instead
        sp.call(['taskkill', '/T', '/F', '/PID',
                str(pid)])
    else:
        os.killpg(os.getpgid(pid), s)


def popen(command, environ, **kw):
    if os.name == "nt":
        # On Windows, the specified env must include a valid SystemRoot
        # Use a current value
        if environ is not None:
            environ["SystemRoot"] = os.environ["SystemRoot"]
        process = sp.Popen(
            ' '.join(command),
            stdout=sp.PIPE,
            stderr=sp.PIPE,
            shell=True,
            env=environ,
            **kw,
        )
    else:
        process = sp.Popen(
            ' '.join(command),
            stdout=sp.PIPE,
            stderr=sp.PIPE,
            shell=True,
            env=environ,
            preexec_fn=os.setpgrp,
            **kw,
        )
    return process


def bootstrapper_name():
    if os.name == "nt":
        return 'bddcli_bootstrapper'
    else:
        return 'bddcli-bootstrapper'


def form_bootstrapper_path(bindir, bootstrapper):
    if os.name == "nt":
        return os.path.join(bindir, bootstrapper, "__init__.py")
    else:
        return os.path.join(bindir, bootstrapper)
