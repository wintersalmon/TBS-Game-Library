from chess.events import MoveChessPieceEvent
from chess.game import ChessGame
from tbs.wrapper import Wrapper


class ChessWrapper(Wrapper):
    def __init__(self, settings, game, events):
        super().__init__(settings, game, events)

    def encode(self):
        return {
            'settings': self.settings,
            # 'game': self.game.encode(),
            'events': [event.encode() for event in self.events],
        }

    @classmethod
    def decode(cls, **kwargs):
        decoded_kwargs = {
            'settings': kwargs['settings'],
            'game': cls.create_game_from_settings(**kwargs['settings']),
            'events': [MoveChessPieceEvent.decode(**e_kwargs) for e_kwargs in kwargs['events']]
        }

        return cls(**decoded_kwargs)

    @classmethod
    def create_game_from_settings(cls, **settings):
        return ChessGame.create(**settings)

    @classmethod
    def create(cls, **kwargs):
        settings = kwargs
        game = cls.create_game_from_settings(**settings)
        events = list()
        return cls(settings=settings, game=game, events=events)
