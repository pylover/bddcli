import abc

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
        pass


