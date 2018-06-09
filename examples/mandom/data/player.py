from typing import Iterable

import collections

from tbs.player import Player as BasePlayer
from tbs.utils import SerializableMixin


class Player(BasePlayer):

    def __init__(self,
                 name: str,
                 victory_point: int = 0,
                 life_point: int = 2):
        super(Player, self).__init__(name=name)
        self.victory_point = victory_point
        self.life_point = life_point

    def __str__(self):
        return 'Player({})'.format(self.name)

    def encode(self):
        return {
            'name': self.name,
            'victory_point': self.victory_point,
            'life_point': self.life_point,
        }

    @classmethod
    def decode(cls, **kwargs):
        name = kwargs['name']
        victory_point = kwargs['victory_point']
        life_point = kwargs['life_point']
        return cls(name=name, victory_point=victory_point, life_point=life_point)


class PlayerTurnTracker(SerializableMixin):

    def __init__(self,
                 players: Iterable[int],
                 disabled_players: Iterable[int] = None):
        self._players = collections.deque(players)

        if disabled_players is None:
            self._disabled_players = collections.deque()
        else:
            self._disabled_players = collections.deque(disabled_players)

    def __len__(self):
        return len(self._players)

    def __getitem__(self, item):
        return self._players[item]

    def __iter__(self):
        for p in self._players[:]:
            yield p

    @property
    def players(self):
        return list(self._players)

    @property
    def disabled_players(self):
        return list(self._disabled_players)

    @property
    def current_player(self):
        return self._players[0]

    def update_turn_forward(self):
        p = self._players.popleft()
        self._players.append(p)

    def update_turn_backward(self):
        p = self._players.pop()
        self._players.appendleft(p)

    def update_turn_forward_and_disable_player(self):
        p = self._players.popleft()
        self._disabled_players.append(p)

    def update_turn_backward_and_enable_player(self):
        p = self._disabled_players.pop()
        self._players.appendleft(p)

    def reset_turn_order(self,
                         players: Iterable[int],
                         starting_player: int = 0):

        self._players = collections.deque(players)
        self._disabled_players.clear()

        if starting_player in self.players and self.current_player != starting_player:
            while self.current_player != starting_player:
                self.update_turn_forward()

    def encode(self):
        return {
            'players': self.players,
            'disabled_players': self.disabled_players,
        }

    @classmethod
    def decode(cls, **kwargs):
        players = kwargs['players']
        disabled_players = kwargs['disabled_players']
        return cls(players=players, disabled_players=disabled_players)
