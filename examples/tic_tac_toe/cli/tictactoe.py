class TicTacToeCLIDraw(object):
    TILE_MARKERS = ('O', 'X', ' ')

    @classmethod
    def draw(cls, game):
        status_msg = 'RUNNING' if game.status else 'STOPPED'
        game_status_repr = 'game status: {}'.format(status_msg)

        lines = list()
        for row in game.board.tiles:
            tiles = list()
            for col in row:
                marker = cls.TILE_MARKERS[col]
                tiles.append('[' + marker + ']')
            line = ''.join(tiles)
            lines.append(line)

        print('\n'.join((game_status_repr, *lines)))
