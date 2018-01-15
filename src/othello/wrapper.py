from core.player import Player
from core.wrapper import Wrapper
from othello.events import PlayerPlacementEvent
from othello.game import OthelloGame

GAME_EVENTS = {
    PlayerPlacementEvent.__name__: PlayerPlacementEvent
}


class OthelloWrapper(Wrapper):
    VIEW_MARKERS = [' ', '●', '○']

    def __init__(self, settings, game, events):
        super().__init__(settings, game, events)

    def __repr__(self):
        lines = list()
        for row in range(self.game.board.rows):
            tiles = list()
            for col in range(self.game.board.cols):
                idx = self.game.board.tiles[row][col]
                tile = '[{}]'.format(self.VIEW_MARKERS[idx])
                tiles.append(tile)
            line = ''.join(tiles)
            lines.append(line)
        return '\n'.join(lines)

    def encode(self):
        return {
            'settings': self.settings,
            'game': self.game.encode(),
            'events': [[event.__class__.__name__, event.encode()] for event in self.events],
        }

    @classmethod
    def decode(cls, **kwargs):
        decoded_settings = kwargs['settings']
        decoded_game = OthelloGame.decode(**kwargs['game'])
        decoded_events = list()
        for e in kwargs['events']:

            try:
                event_name, event_data = e
                event = GAME_EVENTS[event_name].decode(**event_data)
            except Exception as e:
                raise e
            else:
                decoded_events.append(event)

        decoded_kwargs = {
            'settings': decoded_settings,
            'game': decoded_game,
            'events': decoded_events
        }

        return cls(**decoded_kwargs)

    @classmethod
    def create(cls, **kwargs):
        settings = kwargs
        players = [Player(p) for p in kwargs['player_names']]
        game = OthelloGame(players=players)
        events = list()
        return cls(settings=settings, game=game, events=events)
