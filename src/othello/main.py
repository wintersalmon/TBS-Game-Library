from othello.errors import InvalidPositionError, InvalidUserInputError, EndOfInputError, PositionHasNoFlipTargetsError
from othello.events import PlayerPlacementEvent
from othello.managers import OthelloCLIManager


def main():
    settings = {
        'player_names': ['tom', 'jerry']
    }
    othello_manager = OthelloCLIManager.create(**settings)

    while othello_manager:
        othello_manager.view()
        try:
            row, col = get_user_input_or_raise_error()
            event = create_set_event(othello_manager.game, row, col)
            othello_manager.update(event)

        except InvalidUserInputError as e:
            print(e.__class__.__name__, e)

        except InvalidPositionError as e:
            print(e.__class__.__name__, e)

        except EndOfInputError:
            print('End of Input, Exit game ...')
            break

    encoded_othello_data = othello_manager.encode()
    decoded_othello_manager = OthelloCLIManager.decode(**encoded_othello_data)
    decoded_othello_manager.view()


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


if __name__ == '__main__':
    main()
