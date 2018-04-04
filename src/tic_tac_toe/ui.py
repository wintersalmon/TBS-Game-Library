from core.error import InvalidPositionError, ExitGameException, InvalidInputError
from core.managers import UpdateManager
from core.ui import CLIReplay, CLIPlay
from settings import SAVE_DIR
from tic_tac_toe.events import PlayerPlacementEvent
from tic_tac_toe.wrapper import TicTacToeCLIWrapper


class TicTacToeCLIReplay(CLIReplay):
    def __init__(self, file_name):
        super().__init__(cls_wrapper=TicTacToeCLIWrapper, save_dir=SAVE_DIR['tic_tac_toe'], file_name=file_name)


class TicTacToeCLIPlay(CLIPlay):
    def __init__(self, file_name=None):
        super().__init__(cls_wrapper=TicTacToeCLIWrapper, save_dir=SAVE_DIR['tic_tac_toe'], file_name=file_name)
        self.manager = None

    def _create_game(self):
        settings = {'player_names': ['tom', 'jerry']}
        wrapper = TicTacToeCLIWrapper.create(**settings)
        return UpdateManager(wrapper=wrapper)

    def _main_loop(self):
        try:
            row, col = self._read_user_event()
            event = PlayerPlacementEvent.create(game=self.manager.wrapper.game, row=row, col=col)
            self.manager.update(event)
        except ExitGameException as e:
            print(e)
            return False
        except InvalidPositionError as e:
            print(e)
        except InvalidInputError as e:
            print(e)

        return self.manager.wrapper.game.status

    def _read_user_event(self):
        values = input('row, col: ').split()

        if len(values) == 0:
            raise ExitGameException('exit game exception')

        try:
            row, col = values
            row, col = int(row), int(col)
            row, col = row - 1, col - 1

        except ValueError:
            raise InvalidInputError('input requires two integers')

        return row, col
