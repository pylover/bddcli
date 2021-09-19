import os
import abc
import sys
from os import path

from .platform_ import (
    bootstrapper_name,
    form_bootstrapper_path,
    popen
)


class Runner(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def run(self, arguments=None, environ=None, **kw):  # pragma: no cover
        pass


class SubprocessRunner(Runner):

    def _findbindir(self):
        bootstrapper = bootstrapper_name()
        for d in sys.path:
            try:
                if bootstrapper in os.listdir(d):
                    return d
            except FileNotFoundError or NotADirectoryError:
                # Nothing guarantees a PATH entry is valid
                pass

    @property
    def bootstrapper(self):
        bootstrapper = bootstrapper_name()
        if 'VIRTUAL_ENV' in os.environ:
            bindir = path.join(os.environ['VIRTUAL_ENV'], 'bin')
        else:  # pragma: no cover
            bindir = self._findbindir()

        return form_bootstrapper_path(bindir, bootstrapper)

    def __init__(self, application, environ=None):
        self.application = application
        self.environ = environ

    def run(self, arguments=None, working_directory=None, environ=None, **kw):
        command = [
            self.bootstrapper,
            self.application.name,
            self.application.address,
            working_directory or '.',
        ]

        if arguments:
            command += arguments

        process = popen(command, environ, **kw)
        return process
