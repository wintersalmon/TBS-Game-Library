from core.status import Status


class OthelloStatus(Status):
    STATUS_CODE_INIT = 0
    STATUS_CODE_RUNNING = 1
    STATUS_CODE_GAME_OVER = 2

    TURN_BLACK = 1
    TURN_WHITE = 2
    TURN_FLIP = 3

    RUNNING_STATUS_CODES = (
        STATUS_CODE_INIT,
        STATUS_CODE_RUNNING,
    )

    def __init__(self, code=STATUS_CODE_INIT, turn=TURN_BLACK):
        super().__init__(code=code)
        self._turn = turn

    def encode(self):
        return {
            'code': self._code,
            'turn': self._turn,
        }

    @property
    def turn(self):
        return self._turn

    @property
    def turn_player(self):
        return self.turn

    def update(self, game):
        self._code, self._turn = self._update_status_code(game)

    def rollback(self, game):
        if self._code == self.STATUS_CODE_GAME_OVER:
            self._code = self.STATUS_CODE_RUNNING
        elif game.board.count == 0:
            self._code = self.STATUS_CODE_INIT
            self._turn = self.TURN_BLACK
        else:
            self._code, self._turn = self._update_status_code(game)

    def _update_status_code(self, game):
        code = self.STATUS_CODE_RUNNING
        turn = self.turn

        if self.turn == self.TURN_BLACK:
            if self._check_white_can_set(game):
                turn = self.TURN_WHITE
            elif self._check_black_can_set(game):
                turn = self.TURN_BLACK
            else:
                code = self.STATUS_CODE_GAME_OVER

        else:
            if self._check_black_can_set(game):
                turn = self.TURN_BLACK
            elif self._check_white_can_set(game):
                turn = self.TURN_WHITE
            else:
                code = self.STATUS_CODE_GAME_OVER

        return code, turn

    def _check_black_can_set(self, game):
        return self._check_can_set(game, self.TURN_BLACK)

    def _check_white_can_set(self, game):
        return self._check_can_set(game, self.TURN_WHITE)

    def _check_can_set(self, game, color):
        for r in range(game.board.rows):
            for c in range(game.board.cols):
                if game.board.find_flip_positions(r, c, color):
                    return True
        return False

    def __bool__(self):
        return self._code in self.RUNNING_STATUS_CODES
