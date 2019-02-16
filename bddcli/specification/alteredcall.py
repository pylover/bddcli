from .call import Call
from ..response import Response


class Unchanged:
    pass


UNCHANGED = Unchanged()


class AlteredCall(Call):

    def __init__(self, base_call, title, positionals=UNCHANGED, optionals=UNCHANGED,
                 flags=UNCHANGED, stdin=UNCHANGED, extra_environ=None,
                 description=None, response: Response=None):

        self.base_call = base_call
        self.diff = {}
        super().__init__(title, description=description, response=response)
        self.stdin = stdin
        self.positionals = positionals
        self.optionals = optionals
        self.flags = flags
        self.extra_environ = extra_environ

    def to_dict(self):
        result = dict(title=self.title)
        result.update(self.diff)

        if self.description is not None:
            result['description'] = self.description

        if self.response is not None:
            result['response'] = self.response.to_dict()

        return result

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

    @stdin.deleter
    def stdin(self):
        del self.diff['stdin']

    @property
    def positionals(self):
        return self.diff.get('positionals', self.base_call.positionals)

    @positionals.setter
    def positionals(self, value):
        self.update_diff('positionals', value)

    @positionals.deleter
    def positionals(self):
        del self.diff['positionals']

    @property
    def optionals(self):
        return self.diff.get('optionals', self.base_call.optionals)

    @optionals.setter
    def optionals(self, value):
        self.update_diff('optionals', value)

    @optionals.deleter
    def optionals(self):
        del self.diff['optionals']

    @property
    def flags(self):
        return self.diff.get('flags', self.base_call.flags)

    @flags.setter
    def flags(self, value):
        self.update_diff('flags', value)

    @flags.deleter
    def flags(self):
        del self.diff['flags']

    @property
    def extra_environ(self):
        return self.diff.get('extra_environ', self.base_call.extra_environ)

    @extra_environ.setter
    def extra_environ(self, value):
        self.update_diff('extra_environ', value)

    @extra_environ.deleter
    def extra_environ(self):
        del self.diff['extra_environ']

