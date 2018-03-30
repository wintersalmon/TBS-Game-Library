from core.functions import save_game, load_game
from settings import TTT_SAVE_DIR
from tic_tac_toe.events import PlayerPlacementEvent
from tic_tac_toe.managers import TicTacToeUpdateManager, TicTacToeReplayManager
from tic_tac_toe.wrapper import TicTacToeWrapper


def main():
    load_game_name = input('load file name(press ENTER to skip: ')
    if load_game_name:
        data = load_game(TTT_SAVE_DIR, load_game_name)
        ttt_wrapper = TicTacToeWrapper.decode(**data)
        msg = 'game loaded'.format(load_game_name)
    else:  # create new game
        # todo : ask user to input player names
        settings = {
            'player_names': ['tom', 'jerry']
        }
        ttt_wrapper = TicTacToeWrapper.create(**settings)
        msg = 'new game'

    ttt_update_manager = TicTacToeUpdateManager(ttt_wrapper)
    print(msg)

    print(ttt_update_manager)
    while main_loop(ttt_update_manager):
        print(ttt_update_manager)

    save_game_name = input('save file name(press ENTER to skip): ')
    if save_game_name:
        save_game(TTT_SAVE_DIR, save_game_name, ttt_wrapper)
        print('game saved', save_game_name)

    print('good bye ~')


def replay():
    load_game_name = input('load file name: ')
    data = load_game(TTT_SAVE_DIR, load_game_name)
    wrapper = TicTacToeWrapper.decode(**data)
    manager = TicTacToeReplayManager(wrapper)

    manager.set_position(0)
    print(manager)
    while replay_loop(manager):
        print(manager)

    print('good bye ~')


def main_loop(update_manager):
    try:
        row, col = read_user_event()
        event = PlayerPlacementEvent.create(game=update_manager.game_wrapper.game, row=row, col=col)
        update_manager.update(event)
    except ValueError as e:
        print(e)
    except EOFError as e:
        return False
    else:
        return update_manager.game_wrapper.game.status


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


# def replay_test():
#     settings = {
#         'player_names': ['tom', 'jerry']
#     }
#     ttt_wrapper = TicTacToeWrapper.create(**settings)
#     ttt_update_manager = TicTacToeUpdateManager(ttt_wrapper)
#
#     event = PlayerPlacementEvent.create(game=ttt_update_manager.game_wrapper.game, row=1, col=1)
#     ttt_update_manager.update(event)
#     print(ttt_update_manager)
#     event = PlayerPlacementEvent.create(game=ttt_update_manager.game_wrapper.game, row=0, col=0)
#     ttt_update_manager.update(event)
#     print(ttt_update_manager)
#
#     event = PlayerPlacementEvent.create(game=ttt_update_manager.game_wrapper.game, row=0, col=1)
#     ttt_update_manager.update(event)
#     print(ttt_update_manager)
#     event = PlayerPlacementEvent.create(game=ttt_update_manager.game_wrapper.game, row=1, col=0)
#     ttt_update_manager.update(event)
#     print(ttt_update_manager)
#
#     event = PlayerPlacementEvent.create(game=ttt_update_manager.game_wrapper.game, row=2, col=0)
#     ttt_update_manager.update(event)
#     print(ttt_update_manager)
#     event = PlayerPlacementEvent.create(game=ttt_update_manager.game_wrapper.game, row=0, col=2)
#     ttt_update_manager.update(event)
#     print(ttt_update_manager)
#
#     event = PlayerPlacementEvent.create(game=ttt_update_manager.game_wrapper.game, row=2, col=1)
#     ttt_update_manager.update(event)
#     print(ttt_update_manager)
#
#     encoded_game_data = ttt_wrapper.encode()
#
#     print('INIT')
#     ttt_wrapper = TicTacToeWrapper.decode(**encoded_game_data)
#     tic_tac_toe_replay_manager = TicTacToeReplayManager(ttt_wrapper)
#     print(tic_tac_toe_replay_manager)
#
#     print('BACKWARD')
#     while tic_tac_toe_replay_manager.get_position() > 0:
#         tic_tac_toe_replay_manager.backward()
#         print(tic_tac_toe_replay_manager)
#
#     print('FORWARD')
#     while tic_tac_toe_replay_manager.get_position() < tic_tac_toe_replay_manager.get_max_position():
#         tic_tac_toe_replay_manager.forward()
#         print(tic_tac_toe_replay_manager)
#
#     print('SET 0')
#     tic_tac_toe_replay_manager.set_position(0)
#     print(tic_tac_toe_replay_manager)
#
#     print('SET 7')
#     tic_tac_toe_replay_manager.set_position(7)
#     print(tic_tac_toe_replay_manager)
#
#     print('SET 4')
#     tic_tac_toe_replay_manager.set_position(4)
#     print(tic_tac_toe_replay_manager)
#
#     print('SET 1')
#     tic_tac_toe_replay_manager.set_position(1)
#     print(tic_tac_toe_replay_manager)


if __name__ == '__main__':
    main()
