from ..headerset import HeaderSet
from ..helpers import normalize_query_string
from ..response import Response
from .call import Call


class FirstCall(Call):

    _stdin = None
    _positionals = None
    _optionals = None
    _flags = None
    _extra_environ = None

    def __init__(self, title, positionals=None, optionals=None, flags=None,
                 stdin=None, extra_environ=None, description=None,
                 response: Response=None):

        super().__init__(title, description=description, response=response)
        self.stdin = stdin
        self.positionals = positionals
        self.optionals = optionals
        self.flags = flags
        self.extra_environ = extra_environ

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
    def optionals(self):
        return self._optionals

    @optionals.setter
    def optionals(self, value):
        self._optionals = value

    @property
    def flags(self):
        return self._flags

    @flags.setter
    def flags(self, value):
        self._flags = value

    @property
    def extra_environ(self):
        return self._extra_environ

    @extra_environ.setter
    def extra_environ(self, value):
        self._extra_environ = value

