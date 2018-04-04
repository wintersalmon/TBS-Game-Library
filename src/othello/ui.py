from core.error import InvalidPositionError, ExitGameException, InvalidInputError
from core.managers import UpdateManager
from core.ui import CLIReplay, CLIPlay
from othello.events import PlayerPlacementEvent
from othello.wrapper import OthelloCLIWrapper
from settings import SAVE_DIR


class OthelloCLIReplay(CLIReplay):
    def __init__(self, file_name):
        super().__init__(cls_wrapper=OthelloCLIWrapper, save_dir=SAVE_DIR['othello'], file_name=file_name)


class OthelloCLIPlay(CLIPlay):
    def __init__(self, file_name=None):
        super().__init__(cls_wrapper=OthelloCLIWrapper, save_dir=SAVE_DIR['tic_tac_toe'], file_name=file_name)

    def _create_game(self):
        settings = {'player_names': ['tom', 'jerry']}
        wrapper = OthelloCLIWrapper.create(**settings)
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

        return bool(self.manager)

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
