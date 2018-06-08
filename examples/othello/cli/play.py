from tbs.error import InvalidPositionError, InvalidInputError, ExitGameException, ApiError
from tbs.cli import CLIPlay
from othello.cli.draw import OthelloCLIDrawMixin
from othello.events import PlayerPlacementEvent
from othello.managers import OthelloUpdateManager


class OthelloCLIPlay(CLIPlay, OthelloCLIDrawMixin):
    def __init__(self):
        super().__init__(cls_manager=OthelloUpdateManager)

    def update(self):
        try:
            event = self._read_user_input_and_create_event()
            self.manager.update(event)
        except ApiError as e:
            print(e)

    def draw(self):
        super().draw()
        game = self.manager.wrapper.game
        self.draw_status(game)
        self.draw_board(game)

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

        except ValueError:
            raise InvalidInputError('input requires two integers')
        else:
            return PlayerPlacementEvent(row=row, col=col)


GameApp = OthelloCLIPlay

# class OthelloCLIAutoPlay(OthelloCLIPlay, OthelloCLIDrawMixin):
#     def __init__(self, file_name=None, wait_time=0, simple_output_mode=False):
#         super().__init__(file_name=file_name)
#         self.wait_time = wait_time
#         self.simple_output_mode = simple_output_mode
#
#     def draw(self):
#         if self.simple_output_mode:
#             self.draw_status(self.manager.wrapper.game)
#         else:
#             super().draw()
#
#     def update(self):
#         super().update()
#         if self.wait_time:
#             time.sleep(self.wait_time)
#
#     def _read_user_input_and_create_event(self):
#         turn_player = self.manager.wrapper.game.status.player
#         board = self.manager.wrapper.game.board
#
#         next_positions = list()
#         for row in range(board.rows):
#             for col in range(board.cols):
#                 flip_positions = board.find_flip_positions(row, col, turn_player)
#                 if flip_positions:
#                     next_positions.append((len(flip_positions), row, col))
#
#         max_flip_positions = sorted(next_positions, reverse=True)[0][0]
#
#         max_positions = [(f, r, c) for f, r, c in next_positions if f == max_flip_positions]
#         selection = random.choice(max_positions)
#
#         row = selection[1]
#         col = selection[2]
#         if not self.simple_output_mode:
#             print('row, col: {} {}'.format(row, col))
#
#         return PlayerPlacementEvent.create(game=self.manager.wrapper.game, row=row, col=col)
#
#     def save_as(self, file_name):
#         self.manager.save(self.save_dir, file_name)
