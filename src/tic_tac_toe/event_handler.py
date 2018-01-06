from collections import MutableSequence


class TicTacToeEventHandler(object):
    def __init__(self, game, events=None):
        self.game = game
        self.events = list() if isinstance(events, MutableSequence) else events

    def update(self, event):
        try:
            event.update(self.game)
        except Exception as e:
            raise e
        else:
            self.events.append(event)
