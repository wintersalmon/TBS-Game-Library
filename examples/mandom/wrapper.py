from mandom.data.events import MandomEventFactory
from mandom.data.game import MandomGame
from tbs.wrapper import Wrapper


class MandomWrapper(Wrapper):
    cls_game = MandomGame
    cls_event_factory = MandomEventFactory
