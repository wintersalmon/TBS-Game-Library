from core.player import Player
from core.wrapper import Wrapper
from tic_tac_toe.events import PlayerPlacementEvent
from tic_tac_toe.game import TicTacToeGame


class TicTacToeWrapper(Wrapper):
    def __init__(self, settings, game, events):
        super().__init__(settings, game, events)

    def encode(self):
        return {
            'settings': self.settings,
            'game': self.game.encode(),
            'events': [event.encode() for event in self.events],
        }

    @classmethod
    def decode(cls, **kwargs):
        decoded_kwargs = {
            'settings': kwargs['settings'],
            'game': TicTacToeGame.decode(**kwargs['game']),
            'events': [PlayerPlacementEvent.decode(**e_kwargs) for e_kwargs in kwargs['events']]
        }

        return cls(**decoded_kwargs)

    @classmethod
    def create(cls, **kwargs):
        settings = kwargs
        players = [Player(p) for p in kwargs['player_names']]
        game = TicTacToeGame(players=players)
        events = list()
        return cls(settings=settings, game=game, events=events)


class TicTacToeCLIDrawWrapper(TicTacToeWrapper):
    TILE_MARKERS = ('O', 'X', ' ')

    def __str__(self):
        status_msg = 'RUNNING' if self.game.status else 'STOPPED'
        game_status_repr = 'game status: {}'.format(status_msg)

        lines = list()
        for row in self.game.board.tiles:
            tiles = list()
            for col in row:
                if col == self.game.players[0].name:
                    marker = self.TILE_MARKERS[0]
                elif col == self.game.players[1].name:
                    marker = self.TILE_MARKERS[1]
                else:
                    marker = self.TILE_MARKERS[2]
                tiles.append('[' + marker + ']')
            line = ''.join(tiles)
            lines.append(line)

        return '\n'.join((game_status_repr, *lines))
