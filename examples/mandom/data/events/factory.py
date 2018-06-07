from mandom.data.events import EventCode
from mandom.data.events.concrete.challenge_dungeon import ChallengeDungeonEvent
from mandom.data.events.concrete.init_round import InitRoundEvent
from mandom.data.events.concrete.turn_add_monster_to_dungeon import TurnAddMonsterToDungeon
from mandom.data.events.concrete.turn_draw import TurnDrawEvent
from mandom.data.events.concrete.turn_fold import TurnFoldEvent
from mandom.data.events.concrete.turn_remove_weapon_from_hero import TurnRemoveWeaponFromHero


class EventFactory(object):
    EVENTS = dict()
    EVENTS_BY_NUMBER = dict()
    EVENTS_BY_STRING = dict()

    @classmethod
    def register(cls, code: EventCode, event):
        cls.EVENTS[code] = event
        cls.EVENTS_BY_NUMBER[int(code.value)] = event
        cls.EVENTS_BY_STRING[code.name] = event

    @classmethod
    def get(cls, code):
        if isinstance(code, EventCode):
            return cls.EVENTS[code]
        elif isinstance(code, int):
            return cls.EVENTS_BY_NUMBER[code]
        elif isinstance(code, str):
            return cls.EVENTS_BY_STRING[code]
        raise NotImplementedError

    @classmethod
    def create(cls, code, *, params=None):
        event_cls = cls.get(code)
        if params is None:
            params = dict()
        return event_cls(**params)

    @classmethod
    def code_keys(cls):
        return cls.EVENTS.keys()

    @classmethod
    def number_keys(cls):
        return cls.EVENTS_BY_NUMBER.keys()

    @classmethod
    def string_keys(cls):
        return cls.EVENTS_BY_STRING.keys()


EventFactory.register(EventCode.CHALLENGE_DUNGEON, ChallengeDungeonEvent)
EventFactory.register(EventCode.TURN_ADD_MONSTER_TO_DUNGEON, TurnAddMonsterToDungeon)
EventFactory.register(EventCode.TURN_REMOVE_WEAPON_FROM_HERO, TurnRemoveWeaponFromHero)
EventFactory.register(EventCode.INIT_ROUND, InitRoundEvent)
EventFactory.register(EventCode.TURN_FOLD, TurnFoldEvent)
EventFactory.register(EventCode.TURN_DRAW, TurnDrawEvent)
