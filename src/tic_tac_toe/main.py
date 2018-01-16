from tic_tac_toe.events import PlayerPlacementEvent
from tic_tac_toe.wrapper import TicTacToeWrapper
from tic_tac_toe.managers import TicTacToeUpdateManager, TicTacToeReplayManager


def main():
    settings = {
        'player_names': ['tom', 'jerry']
    }
    ttt_wrapper = TicTacToeWrapper.create(**settings)
    ttt_update_manager = TicTacToeUpdateManager(ttt_wrapper)

    print(ttt_update_manager)
    while ttt_update_manager:
        try:
            row, col = read_user_event()
            event = PlayerPlacementEvent.create(game=ttt_update_manager.game_wrapper.game, row=row, col=col)
            ttt_update_manager.update(event)
        except ValueError as e:
            print(e)
        except EOFError as e:
            print(e)
            break
        else:
            print(ttt_update_manager)

    encoded_ttt_data = ttt_wrapper.encode()
    decoded_ttt_manager = TicTacToeWrapper.decode(**encoded_ttt_data)
    print(decoded_ttt_manager)


def read_user_event():
    row, col = input('row, col: ').split()
    row, col = int(row), int(col)

    if row == 0 and col == 0:
        raise EOFError

    row, col = row - 1, col - 1

    return row, col


def replay_main():
    settings = {
        'player_names': ['tom', 'jerry']
    }
    ttt_wrapper = TicTacToeWrapper.create(**settings)
    ttt_update_manager = TicTacToeUpdateManager(ttt_wrapper)

    event = PlayerPlacementEvent.create(game=ttt_update_manager.game_wrapper.game, row=1, col=1)
    ttt_update_manager.update(event)
    print(ttt_update_manager)
    event = PlayerPlacementEvent.create(game=ttt_update_manager.game_wrapper.game, row=0, col=0)
    ttt_update_manager.update(event)
    print(ttt_update_manager)

    event = PlayerPlacementEvent.create(game=ttt_update_manager.game_wrapper.game, row=0, col=1)
    ttt_update_manager.update(event)
    print(ttt_update_manager)
    event = PlayerPlacementEvent.create(game=ttt_update_manager.game_wrapper.game, row=1, col=0)
    ttt_update_manager.update(event)
    print(ttt_update_manager)

    event = PlayerPlacementEvent.create(game=ttt_update_manager.game_wrapper.game, row=2, col=0)
    ttt_update_manager.update(event)
    print(ttt_update_manager)
    event = PlayerPlacementEvent.create(game=ttt_update_manager.game_wrapper.game, row=0, col=2)
    ttt_update_manager.update(event)
    print(ttt_update_manager)

    event = PlayerPlacementEvent.create(game=ttt_update_manager.game_wrapper.game, row=2, col=1)
    ttt_update_manager.update(event)
    print(ttt_update_manager)

    encoded_game_data = ttt_wrapper.encode()

    print('INIT')
    ttt_wrapper = TicTacToeWrapper.decode(**encoded_game_data)
    tic_tac_toe_replay_manager = TicTacToeReplayManager(ttt_wrapper)
    print(tic_tac_toe_replay_manager)

    print('BACKWARD')
    while tic_tac_toe_replay_manager.get_position() > 0:
        tic_tac_toe_replay_manager.backward()
        print(tic_tac_toe_replay_manager)

    print('FORWARD')
    while tic_tac_toe_replay_manager.get_position() < tic_tac_toe_replay_manager.get_max_position():
        tic_tac_toe_replay_manager.forward()
        print(tic_tac_toe_replay_manager)

    print('SET 0')
    tic_tac_toe_replay_manager.set_position(0)
    print(tic_tac_toe_replay_manager)

    print('SET 7')
    tic_tac_toe_replay_manager.set_position(7)
    print(tic_tac_toe_replay_manager)

    print('SET 4')
    tic_tac_toe_replay_manager.set_position(4)
    print(tic_tac_toe_replay_manager)

    print('SET 1')
    tic_tac_toe_replay_manager.set_position(1)
    print(tic_tac_toe_replay_manager)


if __name__ == '__main__':
    main()
