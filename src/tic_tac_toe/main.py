from core.error import InvalidPositionError
from tic_tac_toe.events import PlayerPlacementEvent


def main_loop(update_manager):
    try:
        row, col = read_user_event()
        event = PlayerPlacementEvent.create(game=update_manager.wrapper.game, row=row, col=col)
        update_manager.update(event)
    except InvalidPositionError as e:
        print(e)
    except ValueError as e:
        print(e)
    except EOFError as e:
        return False
    else:
        return update_manager.wrapper.game.status


def replay_loop(replay_manager):
    command = input('input command (Exit|Next|Prev|Index) :').lower()
    if command in ('exit', 'e'):
        return False
    elif command in ('next', 'n'):
        replay_manager.forward()
    elif command in ('prev', 'p'):
        replay_manager.backward()
    else:
        try:
            index = int(command)
        except ValueError as e:
            print('invalid command', command)
        else:
            replay_manager.set_position(index)

    return True


def read_user_event():
    row, col = input('row, col: ').split()
    row, col = int(row), int(col)

    if row == 0 and col == 0:
        raise EOFError

    row, col = row - 1, col - 1

    return row, col
