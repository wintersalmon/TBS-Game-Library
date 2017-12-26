from events.placement_event import PlayerPlacementEvent
from tic_tac_toe_manager import TicTacToeManager


def main_turn():
    manager = TicTacToeManager.create(player_one='tom', player_two='jerry', rows=3, cols=3)

    while manager.is_running():
        try:
            event = read_user_event(manager.game.get_turn_player_name())
            manager.update(event)
        except ValueError as e:
            print(e)
        except EOFError as e:
            print(e)
            exit()
        else:
            manager.draw()


def read_user_event(turn_player_name):
    row, col = input('row, col: ').split()
    row, col = int(row), int(col)

    if row == 0 and col == 0:
        raise EOFError

    row, col = row - 1, col - 1
    event = PlayerPlacementEvent.create(player_name=turn_player_name, row=row, col=col)

    return event


if __name__ == '__main__':
    main_turn()
