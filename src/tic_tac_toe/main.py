from tic_tac_toe.events import PlayerPlacementEvent
from tic_tac_toe.manager import TicTacToeManager
from tic_tac_toe.wrappers import TicTacToeCLIWrapper, TicTacToeReplayWrapper


def main():
    settings = {
        'player_names': ['tom', 'jerry']
    }
    tic_tac_toe_manager = TicTacToeManager.create(**settings)
    tic_tac_toe_cli_wrapper = TicTacToeCLIWrapper(tic_tac_toe_manager)

    tic_tac_toe_cli_wrapper.draw()
    while tic_tac_toe_cli_wrapper:
        try:
            event = read_user_event(tic_tac_toe_manager.game.get_turn_player_name())
            tic_tac_toe_manager.update(event)
        except ValueError as e:
            print(e)
        except EOFError as e:
            print(e)
            break
        else:
            tic_tac_toe_cli_wrapper.draw()

    en = tic_tac_toe_manager.encode()
    de = TicTacToeManager.decode(**en)
    de_cli = TicTacToeCLIWrapper(de)
    de_cli.draw()


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

    tic_tac_toe_replay_wrapper = TicTacToeReplayWrapper(tic_tac_toe_manager)
    while tic_tac_toe_replay_wrapper.get_position() > 0:
        tic_tac_toe_replay_wrapper.backward()
        tic_tac_toe_cli_wrapper.draw()


if __name__ == '__main__':
    main()
