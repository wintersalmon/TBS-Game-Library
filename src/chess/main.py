from chess.events import MoveChessPieceEvent
from core.error import EventCreationFailedError, ExitGameException, InvalidInputError
from core.position import Position


def main_loop(update_manager):
    try:
        pos_src, pos_dst = read_user_event()
        event = MoveChessPieceEvent.create(game=update_manager.wrapper.game,
                                           pos_src=pos_src,
                                           pos_dst=pos_dst)
        update_manager.update(event)
    except ExitGameException as e:
        print(e)
        return False
    except InvalidInputError as e:
        print(e)
    except EventCreationFailedError as e:
        print(e)

    return bool(update_manager)


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
    values = input('from(row,col) to(row,col): ').split()

    if len(values) == 0:
        raise ExitGameException('exit game from retrieving empty input')

    try:
        from_row, from_col, to_row, to_col = values
        from_row, from_col, to_row, to_col = int(from_row), int(from_col), int(to_row), int(to_col)
    except ValueError as e:
        raise InvalidInputError('input requires four integers (int>=0): {}'.format(values)) from e
    return Position(row=from_row, col=from_col), Position(row=to_row, col=to_col)
