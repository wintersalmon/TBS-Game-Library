from othello.errors import InvalidPositionError, InvalidUserInputError, EndOfInputError, PositionHasNoFlipTargetsError
from othello.events import PlayerPlacementEvent


def main_loop(update_manager):
    try:
        row, col = get_user_input_or_raise_error()
        event = PlayerPlacementEvent.create(game=update_manager.wrapper.game, row=row, col=col)
        update_manager.update(event)

    except InvalidUserInputError as e:
        print(e.__class__.__name__, e)

    except InvalidPositionError as e:
        print(e.__class__.__name__, e)

    except EndOfInputError:
        print('End of Input, Exit game ...')
        return False

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


def get_user_input_or_raise_error():
    try:
        row, col = input('row, col: ').split()
        row, col = int(row), int(col)
    except ValueError as e:
        raise InvalidUserInputError(e)

    if row == 0 and col == 0:
        raise EndOfInputError

    row, col = row - 1, col - 1

    return row, col


def create_set_event(game, row, col):
    player_num = game.get_turn_player_number()
    player_marker = game.board.SET_MARKERS[player_num]
    flip_positions = game.board.find_flip_positions(row, col, player_marker)
    event = PlayerPlacementEvent.create(row=row, col=col, marker=player_marker, flip_positions=flip_positions)
    if flip_positions:
        return event
    raise PositionHasNoFlipTargetsError(
        'invalid position ({}, {}), has not target to flip'.format(row, col, player_marker))
