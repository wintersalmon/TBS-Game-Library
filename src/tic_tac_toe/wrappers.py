from core.wrapper import GameWrapper


class TicTacToeCLIWrapper(GameWrapper):
    TILE_MARKERS = ('O', 'X', ' ')

    def __init__(self, manager):
        super().__init__(manager)

    def __bool__(self):
        return self.manager.game.status

    def draw(self):
        status_msg = 'RUNNING' if self.manager.game.status else 'STOPPED'
        print('game status: {}'.format(status_msg))

        board_fmt = ''
        for row in self.manager.game.board.tiles:
            for col in row:
                if col == self.manager.game.player_names[0]:
                    marker = self.TILE_MARKERS[0]
                elif col == self.manager.game.player_names[1]:
                    marker = self.TILE_MARKERS[1]
                else:
                    marker = self.TILE_MARKERS[2]
                board_fmt += '[' + marker + ']'
            board_fmt += '\n'
        print(board_fmt)
