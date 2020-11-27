import subprocess as sp
from abc import ABCMeta, abstractmethod

from .runners import SubprocessRunner


class Call(metaclass=ABCMeta):

    def __init__(self, description=None):
        self.description = description
        self.process = None

    def invoke(self, application):
        self.process = SubprocessRunner(application).run(
            arguments=self.arguments,
            stdin=sp.PIPE,
            working_directory=self.working_directory,
            environ=self.environ,
            encoding=None if isinstance(self.stdin, bytes) else 'UTF-8',
        )

    def conclude(self, application):
        if self.process is None:
            self.invoke(application)

        self.communicate()

    def communicate(self, stdin=None, timeout=None):
        self.stdout, self.stderr = self.process.communicate(
            input=stdin or self.stdin,
            timeout=timeout
        )

    @property
    def status(self):
        return None if self.process is None else self.process.returncode

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
    def arguments(self) -> str:  # pragma: no cover
        pass

    @arguments.setter
    @abstractmethod
    def arguments(self, value):  # pragma: no cover
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
    _arguments = None
    _environ = None
    _working_directory = None

    def __init__(self, arguments=None, stdin=None, working_directory=None,
                 environ=None, description=None):

        super().__init__(description=description)
        self.stdin = stdin
        self.arguments = \
            arguments.split(' ') if isinstance(arguments, str) else arguments
        self.working_directory = working_directory
        self.environ = environ

    @property
    def stdin(self):
        return self._stdin

    @stdin.setter
    def stdin(self, value):
        self._stdin = value

    @property
    def arguments(self):
        return self._arguments

    @arguments.setter
    def arguments(self, value):
        self._arguments = value

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
    def __init__(self, base_call, arguments=UNCHANGED, stdin=UNCHANGED,
                 working_directory=UNCHANGED, environ=UNCHANGED,
                 description=None):

        self.base_call = base_call
        self.diff = {}
        super().__init__(description=description)
        self.stdin = stdin
        self.arguments = arguments
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
    def arguments(self):
        return self.diff.get('arguments', self.base_call.arguments)

    @arguments.setter
    def arguments(self, value):
        self.update_diff('arguments', value)

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
