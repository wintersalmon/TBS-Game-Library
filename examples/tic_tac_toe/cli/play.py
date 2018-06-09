from tbs.cli import CLIPlay
from tbs.error import ExitGameException, InvalidInputError, ApiError
from tic_tac_toe.cli.tictactoe import TicTacToeCLIDraw
from tic_tac_toe.data.events import PlayerPlacementEvent
from tic_tac_toe.managers import TicTacToeUpdateManager


class GameApp(CLIPlay):
    def __init__(self):
        super().__init__(cls_manager=TicTacToeUpdateManager)

    def update(self):
        try:
            event = self._read_user_input_and_create_event()
            self.manager.update(event)
        except ApiError as e:
            print(e)

    def draw(self):
        self._draw_game_play_status()
        TicTacToeCLIDraw.draw(self.manager.wrapper.game)

    def status(self):
        return bool(self.manager.wrapper.game.status)

    def _create_game_settings(self):
        return {'player_names': ['tom', 'jerry']}

    def _read_user_input_and_create_event(self):
        turn_player = self.manager.wrapper.game.status.turn_player
        values = input('row, col: ').split()

        if len(values) == 0:
            raise ExitGameException('exit game exception')

        try:
            row, col = values
            row, col = int(row), int(col)
            row, col = row - 1, col - 1

        except ValueError:
            raise InvalidInputError('input requires two integers')
        else:
            return PlayerPlacementEvent(player=turn_player, row=row, col=col)
