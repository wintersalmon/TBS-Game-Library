from core.status import TurnStatus


class TTTStatus(TurnStatus):
    STATUS_CODE_GAME_INIT = 0
    STATUS_CODE_GAME_RUNNING = 1
    STATUS_CODE_GAME_OVER = 2

    RUNNING_STATUS_CODES = (
        STATUS_CODE_GAME_INIT,
        STATUS_CODE_GAME_RUNNING,
    )

    def __init__(self, code=STATUS_CODE_GAME_INIT, turn=0):
        super().__init__(code=code, turn=turn)

    @property
    def turn_player(self):
        return self.turn % 2

    def update(self, game):
        super().update(game)
        self._update_status_code(game)

    def rollback(self, game):
        super().rollback(game)
        self._update_status_code(game)

    def _update_status_code(self, game):
        if self._find_board_bingo(game.board):
            self._code = self.STATUS_CODE_GAME_OVER
        else:
            self._code = self.STATUS_CODE_GAME_RUNNING

    def _find_board_bingo(self, board):
        # horizontal
        for row in board.tiles:
            if (board.INIT_TILE_VALUE not in row) and len(set(row)) == 1:
                return True

        # vertical
        for col_idx in range(board.cols):
            patterns = set()
            for row_idx in range(board.rows):
                patterns.add(board.tiles[row_idx][col_idx])

            if (board.INIT_TILE_VALUE not in patterns) and len(patterns) == 1:
                return True

        # diagonal left-top right-bottom
        patterns = set()
        for row_idx in range(board.rows):
            for col_idx in range(board.cols):
                if row_idx == col_idx:
                    patterns.add(board.tiles[row_idx][col_idx])

        if (board.INIT_TILE_VALUE not in patterns) and len(patterns) == 1:
            return True

        # diagonal left-bottom right-top
        patterns = set()
        for row_idx in range(board.rows):
            for col_idx in range(board.cols):
                if (row_idx + col_idx) == 2:
                    patterns.add(board.tiles[row_idx][col_idx])

        if (board.INIT_TILE_VALUE not in patterns) and len(patterns) == 1:
            return True

        return False

    def __bool__(self):
        return self._code in self.RUNNING_STATUS_CODES
