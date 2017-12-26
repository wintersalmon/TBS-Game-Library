class Player(object):
    def __init__(self, name, marker):
        self.name = name
        self.marker = marker

    def __repr__(self):
        return 'Player({})'.format(self.name)
