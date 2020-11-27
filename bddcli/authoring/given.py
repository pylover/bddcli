import os
import signal

from ..context import Context
from ..calls import FirstCall, AlteredCall, Call
from .story import Story
from .manipulation import Manipulator


class Given(Story, Context):

    def __init__(self, application, *args, nowait=False, **kwargs):
        self.application = application
        self.nowait = nowait
        base_call = FirstCall(*args, **kwargs)
        self.invoke(base_call)
        super().__init__(base_call)

    def invoke(self, call):
        if self.nowait:
            call.invoke(self.application)
        else:
            call.conclude(self.application)

    def kill(self, s=signal.SIGTERM):
        call = self.current_call
        os.killpg(os.getpgid(call.process.pid), s)

    def wait(self, stdin=None, timeout=None):
        call = self.current_call
        call.communicate(stdin=stdin, timeout=timeout)

    @property
    def current_call(self) -> Call:
        if self.calls:
            return self.calls[-1]
        else:
            return self.base_call

    def when(self, *args, record=True, **kwargs):

        # Checking for list manipulators if any
        # Checking for dictionary manipulators if any
        args = list(args)
        if args:
            arguments = args.pop(0)
            if isinstance(arguments, str):
                arguments = arguments.split(' ')

            kwargs['arguments'] = arguments

        for k, v in kwargs.items():
            if isinstance(v, Manipulator):
                base_arguments = getattr(self.base_call, k)
                if base_arguments:
                    clone = base_arguments.copy()
                else:
                    clone = []
                v.apply(clone)
                kwargs[k] = clone

        new_call = AlteredCall(self.base_call, *args, **kwargs)
        self.invoke(new_call)
        if record:
            self.calls.append(new_call)

        return new_call
