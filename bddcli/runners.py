import io
import abc
import sys

from .response import Response


class Connector(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def run(self, positionals=None, optionals=None, flags=None, stdin=None,
            environ=None, **kw) -> Response:
        pass


class FunctionRunner(Connector):
    def __init__(self, function, environ=None):
        self.function = function
        self.environ = environ

    def run(self, positionals=None, optionals=None, flags=None, stdin=None,
            extra_environ=None, **kw) -> Response:
        # Backup
        stdout_backup = sys.stdout
        stderr_backup = sys.stderr

        sys.stdout = out = io.StringIO()
        sys.stderr = err = io.StringIO()

        status = self.function()
        
        sys.stdout = stdout_backup
        sys.stderr = stderr_backup

        return Response(status, out.getvalue(), err.getvalue())

