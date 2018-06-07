from enum import Enum, auto


class StatusCode(Enum):
    GAME_INIT = auto()
    ROUND = auto()
    TURN = auto()
    CHALLENGE = auto()
    GAME_OVER = auto()
