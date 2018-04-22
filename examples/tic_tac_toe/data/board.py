from tbs.board import Board


class TTTBoard(Board):
    INIT_TILE_VALUE = -1

    def __init__(self, *, tiles=None):
        super().__init__(rows=3, cols=3, init_value=self.INIT_TILE_VALUE, tiles=tiles)

    def encode(self):
        return {
            'tiles': self.tiles
        }

    @classmethod
    def decode(cls, **kwargs):
        tiles = kwargs['tiles']
        return cls(tiles=tiles)
