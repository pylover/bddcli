"""Test scenario authoring stuff."""

from ..proxy import ObjectProxy
from ..calls import FirstCall, AlteredCall, Call

from .story import Story
from .given import Given
from .manipulation import Manipulator, Append, Remove, Update, \
    CompositeManipulatorInitializer


story = ObjectProxy(Given.get_current)
status = ObjectProxy(lambda: story.current_call.status)
stdout = ObjectProxy(lambda: story.current_call.stdout)
stderr = ObjectProxy(lambda: story.current_call.stderr)
given = CompositeManipulatorInitializer()


def when(*args, **kwargs):
    return story.when(*args, **kwargs)
