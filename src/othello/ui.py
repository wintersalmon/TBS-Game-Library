import random
import time

from core.error import InvalidPositionError, ExitGameException, InvalidInputError
from core.ui import CLIReplay, CLIPlay
from othello.events import PlayerPlacementEvent
from othello.wrapper import OthelloWrapper
from settings import SAVE_DIR


class OthelloCLIDraw(object):
    VIEW_MARKERS = [' ', '●', '○', '-']

    @classmethod
    def draw(cls, game):
        is_game_running = bool(game.status)
        turn_player = game.status.turn_player

        lines = list()

        status_msg = 'RUNNING' if is_game_running else 'STOPPED'
        lines.append('game status: {}'.format(status_msg))

        turn_msg = 'Black' if turn_player == 1 else 'White'
        lines.append('current turn: {}'.format(turn_msg))

        lines.append('   ' + ''.join(' {} '.format(c) for c in range(game.board.cols)))

        next_positions = list()

        tile_count = {
            1: 0,
            2: 0,
        }

        for row in range(game.board.rows):
            tiles = list()
            tiles.append(' {} '.format(row))

            for col in range(game.board.cols):
                marker = game.board.tiles[row][col]
                if marker != 0:
                    tile_count[marker] += 1
                    tile = ' {} '.format(cls.VIEW_MARKERS[marker])
                else:
                    positions = game.board.find_flip_positions(row, col, turn_player)
                    if positions:
                        tile = '[ ]'
                        next_positions.append((len(positions), row, col))
                    else:
                        tile = '   '

                tiles.append(tile)

            line = ''.join(tiles)
            lines.append(line)

        lines.append(' '.join('[{:<2}: {},{}]'.format(f, r, c) for f, r, c in sorted(next_positions, reverse=True)))
        lines.append('Black({}) vs White({})'.format(tile_count[1], tile_count[2]))

        print('\n'.join(lines))


class OthelloCLIReplay(CLIReplay):
    def __init__(self, file_name):
        super().__init__(cls_wrapper=OthelloWrapper, save_dir=SAVE_DIR['othello'], file_name=file_name)

    def draw(self):
        super().draw()
        OthelloCLIDraw.draw(self.manager.wrapper.game)


class OthelloCLIPlay(CLIPlay):
    def __init__(self, file_name=None):
        super().__init__(cls_wrapper=OthelloWrapper, save_dir=SAVE_DIR['othello'], file_name=file_name)

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
        OthelloCLIDraw.draw(self.manager.wrapper.game)

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


class OthelloCLIAutoPlay(OthelloCLIPlay):
    def __init__(self, file_name=None, wait_time=0, is_simple_draw=True):
        super().__init__(file_name=file_name)
        self.wait_time = wait_time
        self.is_simple_draw = is_simple_draw

    def draw(self):
        if self.is_simple_draw:
            self.simple_draw()
        else:
            super().draw()

    def simple_draw(self):
        events = len(self.manager.wrapper.events)
        player = 'Black' if self.manager.wrapper.game.status.turn_player == 1 else 'White'
        print('events {events:02}, {player}'.format(events=events, player=player))

    def update(self):
        super().update()
        if self.wait_time:
            time.sleep(self.wait_time)

    def _read_user_input_and_create_event(self):
        turn_player = self.manager.wrapper.game.status.turn_player
        board = self.manager.wrapper.game.board

        next_positions = list()
        for row in range(board.rows):
            for col in range(board.cols):
                flip_positions = board.find_flip_positions(row, col, turn_player)
                if flip_positions:
                    next_positions.append((len(flip_positions), row, col))

        max_flip_positions = sorted(next_positions, reverse=True)[0][0]

        max_positions = [(f, r, c) for f, r, c in next_positions if f == max_flip_positions]
        selection = random.choice(max_positions)

        row = selection[1]
        col = selection[2]
        if not self.is_simple_draw:
            print('row, col: {} {}'.format(row, col))

        return PlayerPlacementEvent.create(game=self.manager.wrapper.game, row=row, col=col)

    def save_as(self, file_name):
        self.manager.save(self.save_dir, file_name)
