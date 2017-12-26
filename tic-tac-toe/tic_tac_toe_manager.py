from tic_tac_toe import TicTacToe


class TicTacToeManager(object):
    TILE_MARKERS = ('O', 'X', ' ')

    def __init__(self, player_one, player_two, rows, cols):
        self.game = TicTacToe(player_one, player_two, rows, cols)
        self.events = list()
        self.player_names = (player_one, player_two)

    def update(self, event):
        try:
            event.update(self.game)
        except Exception as e:
            raise e
        else:
            self.events.append(event)

    def draw(self):
        status_msg = 'RUNNING' if self.game.status else 'STOPPED'
        print('game status: {}'.format(status_msg))
        print('total events: {}'.format(len(self.events)))
        print('last event: {}'.format(self.events[-1]))

        board_fmt = ''
        for row in self.game.board.tiles:
            for col in row:
                if col == self.player_names[0]:
                    marker = self.TILE_MARKERS[0]
                elif col == self.player_names[1]:
                    marker = self.TILE_MARKERS[1]
                else:
                    marker = self.TILE_MARKERS[2]
                board_fmt += '[' + marker + ']'
            board_fmt += '\n'
        print(board_fmt)
