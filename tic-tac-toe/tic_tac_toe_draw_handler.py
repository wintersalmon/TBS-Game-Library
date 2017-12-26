class TicTacToeDrawHandler(object):
    TILE_MARKERS = ('O', 'X', ' ')

    def __init__(self, game):
        self.game = game

    def draw(self):
        status_msg = 'RUNNING' if self.game.status else 'STOPPED'
        print('game status: {}'.format(status_msg))

        board_fmt = ''
        for row in self.game.board.tiles:
            for col in row:
                if col == self.game.player_names[0]:
                    marker = self.TILE_MARKERS[0]
                elif col == self.game.player_names[1]:
                    marker = self.TILE_MARKERS[1]
                else:
                    marker = self.TILE_MARKERS[2]
                board_fmt += '[' + marker + ']'
            board_fmt += '\n'
        print(board_fmt)
