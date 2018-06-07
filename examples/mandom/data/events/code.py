from enum import Enum, auto


class EventCode(Enum):
    INIT_ROUND = auto()
    CHALLENGE_DUNGEON = auto()
    TURN_FOLD = auto()
    TURN_DRAW = auto()
    TURN_ADD_MONSTER_TO_DUNGEON = auto()
    TURN_REMOVE_WEAPON_FROM_HERO = auto()
