from core.error import InvalidPositionError, ExitGameException, InvalidInputError
from core.ui import CLIReplay, CLIPlay
from settings import SAVE_DIR
from tic_tac_toe.events import PlayerPlacementEvent
from tic_tac_toe.wrapper import TicTacToeWrapper


class TicTacToeCLIDraw(object):
    TILE_MARKERS = ('O', 'X', ' ')

    @classmethod
    def draw(cls, game):
        status_msg = 'RUNNING' if game.status else 'STOPPED'
        game_status_repr = 'game status: {}'.format(status_msg)

        lines = list()
        for row in game.board.tiles:
            tiles = list()
            for col in row:
                marker = cls.TILE_MARKERS[col]
                tiles.append('[' + marker + ']')
            line = ''.join(tiles)
            lines.append(line)

        print('\n'.join((game_status_repr, *lines)))


class TicTacToeCLIReplay(CLIReplay):
    def __init__(self, file_name):
        super().__init__(cls_wrapper=TicTacToeWrapper, save_dir=SAVE_DIR['tic_tac_toe'], file_name=file_name)

    def draw(self):
        super().draw()
        TicTacToeCLIDraw.draw(self.manager.wrapper.game)


class TicTacToeCLIPlay(CLIPlay):
    def __init__(self, file_name=None):
        super().__init__(cls_wrapper=TicTacToeWrapper, save_dir=SAVE_DIR['tic_tac_toe'], file_name=file_name)

    def update(self):
        try:
            event = self._read_user_input_and_create_event()
            self.manager.update(event)
        except InvalidPositionError as e:
            print(e)
        except InvalidInputError as e:
            print(e)

    def draw(self):
        super().draw()
        TicTacToeCLIDraw.draw(self.manager.wrapper.game)

    def status(self):
        return bool(self.manager.wrapper.game.status)

    def _create_game_settings(self):
        return {'player_names': ['tom', 'jerry']}

    def _read_user_input_and_create_event(self):
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
            return PlayerPlacementEvent.create(game=self.manager.wrapper.game, row=row, col=col)
