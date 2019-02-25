import re
import sys
from abc import ABCMeta, abstractmethod

from .response import Response
from .runners import SubprocessRunner


class Call(metaclass=ABCMeta):

    def __init__(self, title, description=None, response=None):
        self.title = title
        self.description = description
        self.response = response

    def invoke(self, application) -> Response:
        return SubprocessRunner(application).run(
            positionals=self.positionals,
            flags=self.flags,
            stdin=self.stdin,
            working_directory=self.working_directory,
            environ=self.environ
        )

    def conclude(self, application):
        if self.response is None:
            self.response = self.invoke(application)

    @property
    @abstractmethod
    def stdin(self) -> str:  # pragma: no cover
        pass

    @stdin.setter
    @abstractmethod
    def stdin(self, value):  # pragma: no cover
        pass

    @property
    @abstractmethod
    def positionals(self) -> str:  # pragma: no cover
        pass

    @positionals.setter
    @abstractmethod
    def positionals(self, value):  # pragma: no cover
        pass

    @property
    @abstractmethod
    def flags(self) -> dict:  # pragma: no cover
        pass

    @flags.setter
    @abstractmethod
    def flags(self, value):  # pragma: no cover
        pass

    @property
    @abstractmethod
    def environ(self) -> dict:  # pragma: no cover
        pass

    @environ.setter
    @abstractmethod
    def environ(self, value):  # pragma: no cover
        pass


class FirstCall(Call):

    _stdin = None
    _positionals = None
    _flags = None
    _environ = None
    _working_directory = None

    def __init__(self, title, positionals=None, flags=None, stdin=None,
                 working_directory=None, environ=None, description=None,
                 response=None):

        super().__init__(title, description=description, response=response)
        self.stdin = stdin
        self.positionals = positionals
        self.flags = flags
        self.working_directory = working_directory
        self.environ = environ

    @property
    def stdin(self):
        return self._stdin

    @stdin.setter
    def stdin(self, value):
        self._stdin = value

    @property
    def positionals(self):
        return self._positionals

    @positionals.setter
    def positionals(self, value):
        self._positionals = value

    @property
    def flags(self):
        return self._flags

    @flags.setter
    def flags(self, value):
        self._flags = value

    @property
    def working_directory(self):
        return self._working_directory

    @working_directory.setter
    def working_directory(self, value):
        self._working_directory = value

    @property
    def environ(self):
        return self._environ

    @environ.setter
    def environ(self, value):
        self._environ = value


class Unchanged:
    pass


UNCHANGED = Unchanged()


class AlteredCall(Call):
    def __init__(self, base_call, title, positionals=UNCHANGED,
                 flags=UNCHANGED, stdin=UNCHANGED, working_directory=None,
                 environ=None, description=None, response=None):

        self.base_call = base_call
        self.diff = {}
        super().__init__(title, description=description, response=response)
        self.stdin = stdin
        self.positionals = positionals
        self.flags = flags
        self.working_directory = working_directory
        self.environ = environ

    def update_diff(self, key, value):
        if value is UNCHANGED:
            self.diff.pop(key, None)
            return

        self.diff[key] = value

    @property
    def stdin(self):
        return self.diff.get('stdin', self.base_call.stdin)

    @stdin.setter
    def stdin(self, value):
        self.update_diff('stdin', value)

    @property
    def positionals(self):
        return self.diff.get('positionals', self.base_call.positionals)

    @positionals.setter
    def positionals(self, value):
        self.update_diff('positionals', value)

    @property
    def flags(self):
        return self.diff.get('flags', self.base_call.flags)

    @flags.setter
    def flags(self, value):
        self.update_diff('flags', value)

    @property
    def working_directory(self):
        return self.diff.get(
            'working_directory',
            self.base_call.working_directory
        )

    @working_directory.setter
    def working_directory(self, value):
        self.update_diff('working_directory', value)

    @property
    def environ(self):
        return self.diff.get('environ', self.base_call.environ)

    @environ.setter
    def environ(self, value):
        self.update_diff('environ', value)

