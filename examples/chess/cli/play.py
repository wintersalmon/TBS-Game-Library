from chess.cli.chess import ChessCLIDrawMixin
from chess.events import MoveChessPieceEvent
from chess.managers import ChessUpdateManager
from tbs.cli import CLIPlay
from tbs.error import ExitGameException, InvalidInputError, ApiError
from tbs.position import Position


class ChessCLIPlay(CLIPlay):
    def __init__(self):
        super().__init__(cls_manager=ChessUpdateManager)

    def update(self):
        try:
            event = self._read_user_input_and_create_event()
            self.manager.update(event)
        except ApiError as e:
            print(e)

    def _read_user_input_and_create_event(self):
        values = input('from(row,col) to(row,col): ').split()

        if len(values) == 0:
            raise ExitGameException('exit game from retrieving empty input')

        try:
            from_row, from_col, to_row, to_col = values
            from_row, from_col, to_row, to_col = int(from_row), int(from_col), int(to_row), int(to_col)
        except ValueError as e:
            raise InvalidInputError('input requires four integers (int>=0): {}'.format(values)) from e

        pos_src = Position(row=from_row, col=from_col)
        pos_dst = Position(row=to_row, col=to_col)

        return MoveChessPieceEvent(pos_src=pos_src, pos_dst=pos_dst)

    def _create_game_settings(self):
        return {'player_names': ['tom', 'jerry']}

    def status(self):
        return bool(self.manager)

    def draw(self):
        super().draw()
        ChessCLIDrawMixin.draw(self.manager.wrapper.game)


GameApp = ChessCLIPlay
