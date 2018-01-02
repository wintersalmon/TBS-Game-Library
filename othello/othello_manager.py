class OthelloManager(object):
    def __init__(self, player_one, player_two):
        self.players = list()

    @classmethod
    def create(cls, player_one, player_two):
        return OthelloManager(player_one, player_two)
