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
                if col == self.manager.game.players[0].name:
                    marker = self.TILE_MARKERS[0]
                elif col == self.manager.game.players[1].name:
                    marker = self.TILE_MARKERS[1]
                else:
                    marker = self.TILE_MARKERS[2]
                board_fmt += '[' + marker + ']'
            board_fmt += '\n'
        print(board_fmt)


class TicTacToeReplayWrapper(GameWrapper):
    def __init__(self, manager):
        super().__init__(manager)
        self.max_position = len(self.manager.events)
        self.position = self.max_position

    def get_position(self):
        return self.position

    def forward(self):
        if self.position < self.max_position:
            self.position += 1
            event = self.manager.events[self.position]
            event.update(self.manager.game)

    def backward(self):
        if self.position > 0:
            self.position -= 1
            event = self.manager.events[self.position]
            event.rollback(self.manager.game)
