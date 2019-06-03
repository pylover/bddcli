from ..context import Context
from ..calls import FirstCall, AlteredCall, Call
from .story import Story
from .manipulation import Manipulator


class Given(Story, Context):

    def __init__(self, application, *args, **kwargs):
        self.application = application
        base_call = FirstCall(*args, **kwargs)
        base_call.conclude(application)
        super().__init__(base_call)

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
                clone = getattr(self.base_call, k).copy()
                v.apply(clone)
                kwargs[k] = clone

        new_call = AlteredCall(self.base_call, *args, **kwargs)
        new_call.conclude(self.application)
        if record:
            self.calls.append(new_call)

        return new_call

    def __enter__(self):
        return super().__enter__()

    def __exit__(self, exc_type, exc_value, traceback):
        return super().__exit__(exc_type, exc_value, traceback)

    @property
    def response(self):
        return self.current_call.response


