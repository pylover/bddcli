import abc
import subprocess as sp

from .platform_ import Popen, BOOTSTRAPPER_FULLPATH


class Runner(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def run(self, arguments=None, environ=None, **kw):  # pragma: no cover
        pass


class SubprocessRunner(Runner):

    def __init__(self, application, environ=None):
        self.application = application
        self.environ = environ

    def run(self, arguments=None, working_directory=None, environ=None, **kw):
        command = [
            BOOTSTRAPPER_FULLPATH,
            self.application.name,
            self.application.address,
            working_directory or '.',
        ]

        if arguments:
            command += arguments

        process = Popen(
            ' '.join(command),
            stdout=sp.PIPE,
            stderr=sp.PIPE,
            shell=True,
            env=environ,
            **kw,
        )
        return process
