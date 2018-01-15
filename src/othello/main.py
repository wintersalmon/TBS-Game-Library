from othello.errors import InvalidPositionError, InvalidUserInputError, EndOfInputError, PositionHasNoFlipTargetsError
from othello.events import PlayerPlacementEvent
from othello.managers import OthelloUpdateManager, OthelloReplayManager
from othello.wrapper import OthelloWrapper


def main():
    settings = {
        'player_names': ['tom', 'jerry']
    }
    othello_wrapper = OthelloWrapper.create(**settings)
    othello_update_manager = OthelloUpdateManager(othello_wrapper)

    while othello_update_manager:
        othello_update_manager.view()
        try:
            row, col = get_user_input_or_raise_error()
            event = create_set_event(othello_update_manager.game_wrapper.game, row, col)
            othello_update_manager.update(event)

        except InvalidUserInputError as e:
            print(e.__class__.__name__, e)

        except InvalidPositionError as e:
            print(e.__class__.__name__, e)

        except EndOfInputError:
            print('End of Input, Exit game ...')
            break

    encoded_othello_data = othello_update_manager.game_wrapper.game.encode()
    decoded_othello_wrapper = OthelloWrapper.decode(**encoded_othello_data)
    decoded_othello_wrapper.view()


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


def replay_main():
    settings = {
        'player_names': ['tom', 'jerry']
    }
    othello_wrapper = OthelloWrapper.create(**settings)
    othello_update_manager = OthelloUpdateManager(othello_wrapper)

    # othello_manger.view()
    # print(othello_manger.game.board.get(3, 3))
    # print(othello_manger.game.board.get(3, 4))
    # print(othello_manger.game.board.get(4, 3))
    # print(othello_manger.game.board.get(4, 4))
    # othello_manger.game.board.flip(4, 3)
    # othello_manger.view()

    event = create_set_event(othello_wrapper.game, 4, 2)
    othello_update_manager.update(event)
    othello_update_manager.view()

    event = create_set_event(othello_wrapper.game, 3, 2)
    othello_update_manager.update(event)
    othello_update_manager.view()

    event = create_set_event(othello_wrapper.game, 2, 1)
    othello_update_manager.update(event)
    othello_update_manager.view()

    event = create_set_event(othello_wrapper.game, 3, 1)
    othello_update_manager.update(event)
    othello_update_manager.view()

    othello_update_manager.view()
    encoded_game_data = othello_wrapper.encode()

    print('INIT')
    othello_wrapper = OthelloWrapper.decode(**encoded_game_data)
    replay_manger = OthelloReplayManager(othello_wrapper)
    print(replay_manger)
    replay_manger.view()

    print('BACKWARD')
    while replay_manger.get_position() > 0:
        replay_manger.backward()
        print(replay_manger)
        replay_manger.view()

    print('FORWARD')
    while replay_manger.get_position() < replay_manger.get_max_position():
        replay_manger.forward()
        print(replay_manger)
        replay_manger.view()

    print('SET 0')
    replay_manger.set_position(0)
    print(replay_manger)
    replay_manger.view()

    print('SET 4')
    replay_manger.set_position(4)
    print(replay_manger)
    replay_manger.view()

    print('SET 1')
    replay_manger.set_position(1)
    print(replay_manger)
    replay_manger.view()


if __name__ == '__main__':
    main()
