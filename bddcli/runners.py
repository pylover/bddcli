import io
import abc
import sys
import subprocess as sp

from .response import Response


class Runner(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def run(self, positionals=None, optionals=None, flags=None, stdin=None,
            environ=None, **kw) -> Response:
        pass


class SubprocessRunner(Runner):
    bootstrapper = 'bddcli_bootstrapper'

    def __init__(self, application, environ=None):
        self.application = application
        self.environ = environ

    def run(self, positionals=None, optionals=None, flags=None, stdin=None,
            extra_environ=None, working_directory=None, **kw) -> Response:
        result = sp.run(
            [
                self.bootstrapper,
                self.application.name,
                self.application.address,
            ],
            stdin=stdin,
            stdout=sp.PIPE,
            stderr=sp.PIPE,
            shell=True,
            cwd=working_directory,
        )
        return Response(result.returncode, result.stdout, result.stderr)

