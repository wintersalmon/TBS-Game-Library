from core.manager import GameUpdateManager, GameReplayManager


class TicTacToeUpdateManager(GameUpdateManager):
    pass


class TicTacToeReplayManager(GameReplayManager):
    pass

#
#
# class TicTacToeViewableManager(TicTacToeWrapper):
#     TILE_MARKERS = ('O', 'X', ' ')
#
#     def __init__(self, settings, game, events):
#         super().__init__(settings, game, events)
#
#     def __bool__(self):
#         return self.game.status
#
#     def view(self):
#         status_msg = 'RUNNING' if self.game.status else 'STOPPED'
#         print('game status: {}'.format(status_msg))
#
#         board_fmt = ''
#         for row in self.game.board.tiles:
#             for col in row:
#                 if col == self.game.players[0].name:
#                     marker = self.TILE_MARKERS[0]
#                 elif col == self.game.players[1].name:
#                     marker = self.TILE_MARKERS[1]
#                 else:
#                     marker = self.TILE_MARKERS[2]
#                 board_fmt += '[' + marker + ']'
#             board_fmt += '\n'
#         print(board_fmt)
#
#
# class TicTacToeMutableManager(TicTacToeViewableManager):
#     def __init__(self, settings, game, events):
#         super().__init__(settings, game, events)
#
#     def update(self, event):
#         try:
#             event.update(self.game)
#         except Exception as e:
#             raise e
#         else:
#             self.events.append(event)
#
#
# class TicTacToeCLIManager(TicTacToeMutableManager):
#     pass
#
#
# class TicTacToeReplayManager(TicTacToeViewableManager):
#     def __init__(self, settings, game, events):
#         super().__init__(settings, game, events)
#         self._max_position = len(self.events)
#         self._cur_position = self._max_position
#
#     def set_position(self, position):
#         if 0 <= position <= self._max_position:
#             pos_difference = position - self._cur_position
#             pos_offset = abs(pos_difference)
#
#             if pos_difference >= 0:
#                 move_to_direction = self.forward
#             else:
#                 move_to_direction = self.backward
#
#             while pos_offset > 0:
#                 move_to_direction()
#                 pos_offset -= 1
#
#     def get_max_position(self):
#         return self._max_position
#
#     def get_position(self):
#         return self._cur_position
#
#     def forward(self):
#         if self._cur_position < self._max_position:
#             event = self.events[self._cur_position]
#             event.update(self.game)
#             self._cur_position += 1
#             return True
#         raise CustomError('Impossible to move forward')
#
#     def backward(self):
#         if self._cur_position >= 0:
#             event = self.events[self._cur_position - 1]
#             event.rollback(self.game)
#             self._cur_position -= 1
#             return True
#         raise CustomError('Impossible to move backward')
#
#     def __repr__(self):
#         return '{}/{}'.format(self._cur_position, self._max_position)
