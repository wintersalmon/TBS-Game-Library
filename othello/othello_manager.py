from othello import Othello


class OthelloManager(object):
    def __init__(self, game, events):
        self.game = game
        self.events = events

    def update(self, event):
        event.update(self.game)
        self.events.append(event)

    @classmethod
    def create(cls, player_one, player_two):
        othello = Othello(player_one, player_two)
        events = list()
        return OthelloManager(game=othello, events=events)
