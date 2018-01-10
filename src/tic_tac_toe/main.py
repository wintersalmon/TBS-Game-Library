from tic_tac_toe.events import PlayerPlacementEvent
from tic_tac_toe.managers import TicTacToeManager
from tic_tac_toe.managers import TicTacToeReplayManager
from tic_tac_toe.managers import TicTacToeCLIWManager


def main():
    settings = {
        'player_names': ['tom', 'jerry']
    }
    ttt_manager = TicTacToeCLIWManager.create(**settings)

    ttt_manager.draw()
    while ttt_manager:
        try:
            event = read_user_event(ttt_manager.game.get_turn_player_name())
            ttt_manager.update(event)
        except ValueError as e:
            print(e)
        except EOFError as e:
            print(e)
            break
        else:
            ttt_manager.draw()

    encoded_ttt_data = ttt_manager.encode()
    decoded_ttt_manager = TicTacToeCLIWManager.decode(**encoded_ttt_data)
    decoded_ttt_manager.draw()


def read_user_event(turn_player_name):
    row, col = input('row, col: ').split()
    row, col = int(row), int(col)

    if row == 0 and col == 0:
        raise EOFError

    row, col = row - 1, col - 1
    event = PlayerPlacementEvent.create(player_name=turn_player_name, row=row, col=col)

    return event


def replay_main():
    settings = {
        'player_names': ['tom', 'jerry']
    }
    tic_tac_toe_manager = TicTacToeManager.create(**settings)
    tic_tac_toe_cli_wrapper = TicTacToeCLIWrapper(tic_tac_toe_manager)
    events = [
        PlayerPlacementEvent.create(player_name='tom', row=1, col=1),
        PlayerPlacementEvent.create(player_name='jerry', row=0, col=0),

        PlayerPlacementEvent.create(player_name='tom', row=0, col=1),
        PlayerPlacementEvent.create(player_name='jerry', row=1, col=0),

        PlayerPlacementEvent.create(player_name='tom', row=2, col=0),
        PlayerPlacementEvent.create(player_name='jerry', row=0, col=2),

        PlayerPlacementEvent.create(player_name='tom', row=2, col=1)
    ]

    for event in events:
        tic_tac_toe_manager.update(event)
        tic_tac_toe_cli_wrapper.draw()

    tic_tac_toe_cli_wrapper.draw()
    encoded_game_data = tic_tac_toe_manager.encode()

    print('INIT')
    tic_tac_toe_replay_manager = TicTacToeReplayManager.decode(**encoded_game_data)
    print(tic_tac_toe_replay_manager)
    tic_tac_toe_cli_wrapper.draw()

    print('BACKWARD')
    while tic_tac_toe_replay_manager.get_position() > 0:
        tic_tac_toe_replay_manager.backward()
        print(tic_tac_toe_replay_manager)
        tic_tac_toe_cli_wrapper.draw()

    print('FORWARD')
    while tic_tac_toe_replay_manager.get_position() < tic_tac_toe_replay_manager.get_max_position():
        tic_tac_toe_replay_manager.forward()
        print(tic_tac_toe_replay_manager)
        tic_tac_toe_cli_wrapper.draw()

    print('SET 0')
    tic_tac_toe_replay_manager.set_position(0)
    print(tic_tac_toe_replay_manager)
    tic_tac_toe_cli_wrapper.draw()

    print('SET 7')
    tic_tac_toe_replay_manager.set_position(7)
    print(tic_tac_toe_replay_manager)
    tic_tac_toe_cli_wrapper.draw()

    print('SET 4')
    tic_tac_toe_replay_manager.set_position(4)
    print(tic_tac_toe_replay_manager)
    tic_tac_toe_cli_wrapper.draw()

    print('SET 1')
    tic_tac_toe_replay_manager.set_position(1)
    print(tic_tac_toe_replay_manager)
    tic_tac_toe_cli_wrapper.draw()


if __name__ == '__main__':
    main()
