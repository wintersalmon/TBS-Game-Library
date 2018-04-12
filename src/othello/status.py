from core.status import TurnStatus


class OthelloStatus(TurnStatus):
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

    def __init__(self, code=STATUS_CODE_INIT, turn=0, player=TURN_BLACK):
        super().__init__(code=code, turn=turn)
        self._player = player

    def encode(self):
        return {
            'code': self._code,
            'turn': self._turn,
            'player': self._player,
        }

    @property
    def turn(self):
        return self._turn

    @property
    def player(self):
        return self._player

    def update(self, game):
        super().update(game)
        self._code, self._player = self._update_status_code_and_player(game)

    def rollback(self, game):
        super().rollback(game)
        if self._code == self.STATUS_CODE_GAME_OVER:
            self._code = self.STATUS_CODE_RUNNING
        elif self.turn == 0:
            self._code = self.STATUS_CODE_INIT
            self._player = self.TURN_BLACK
        else:
            self._code, self._player = self._update_status_code_and_player(game)

    def _update_status_code_and_player(self, game):
        code = self.STATUS_CODE_RUNNING
        player = self.player

        if self.player == self.TURN_BLACK:
            if self._check_white_can_set(game):
                player = self.TURN_WHITE
            elif self._check_black_can_set(game):
                player = self.TURN_BLACK
            else:
                code = self.STATUS_CODE_GAME_OVER

        else:
            if self._check_black_can_set(game):
                player = self.TURN_BLACK
            elif self._check_white_can_set(game):
                player = self.TURN_WHITE
            else:
                code = self.STATUS_CODE_GAME_OVER

        return code, player

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
