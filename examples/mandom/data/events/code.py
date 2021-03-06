from enum import Enum


class EventCode(Enum):
    INIT_ROUND = 1000
    TURN_DRAW = 2001
    TURN_FOLD = 2002
    CHALLENGE_DUNGEON = 2003
    TURN_ADD_MONSTER_TO_DUNGEON = 3001
    TURN_REMOVE_WEAPON_FROM_HERO = 3002
