import re
import sys
from abc import ABCMeta, abstractmethod

from ..exceptions import CallVerifyError
from ..response import Response


class Call(metaclass=ABCMeta):

    def __init__(self, title, description=None, response=None):
        self.title = title
        self.description = description
        if response is not None and not isinstance(response, Response):
            response = Response(**response)
        self.response = response

    def to_dict(self):
        result = dict(
            title=self.title,
        )

        if self.stdin is not None:
            result['stdin'] = self.stdin

        if self.positionals is not None:
            result['positionals'] = self.positionals

        if self.optionals is not None:
            result['optionals'] = self.optionals

        if self.flags is not None:
            result['flags'] = self.flags

        if self.response is not None:
            result['response'] = self.response.to_dict()

        return result

    def invoke(self, application) -> Response:
        return WSGIConnector(application).request(
            self.positionals,
            self.optionals,
            self.flags,
            self.stdin,
            self.extra_environ
        )

    def verify(self, application):
        response = self.invoke(application)
        if self.response != response:
            raise CallVerifyError()

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
    def optionals(self):  # pragma: no cover
        pass

    @optionals.setter
    @abstractmethod
    def optionals(self, value):  # pragma: no cover
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
    def extra_environ(self) -> dict:  # pragma: no cover
        pass

    @extra_environ.setter
    @abstractmethod
    def extra_environ(self, value):  # pragma: no cover
        pass

