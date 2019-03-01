
from ..proxy import ObjectProxy
from ..calls import FirstCall, AlteredCall, Call

from .story import Story
from .given import Given
from .manipulation import Manipulator, Append, Remove, Update, \
    CompositeManipulatorInitializer


story = ObjectProxy(Given.get_current)
status = ObjectProxy(lambda: story.response.status)
stdout = ObjectProxy(lambda: story.response.stdout)
stderr = ObjectProxy(lambda: story.response.stderr)
given = CompositeManipulatorInitializer()


def when(*args, **kwargs):
    return story.when(*args, **kwargs)

