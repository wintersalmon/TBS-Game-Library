from events.placement_event import PlayerPlacementEvent
from tic_tac_toe_manager import TicTacToeManager


def main_turn():
    manager = TicTacToeManager(player_one='tom', player_two='jerry', rows=3, cols=3)
    while manager.game.status:
        # input user command
        try:
            row, col = input('row, col: ').split()
            row, col = int(row), int(col)
        except ValueError as e:
            print(e)
            continue
        else:
            # exit if input is (0, 0)
            if row == 0 and col == 0:
                exit(0)
            else:
                row, col = row - 1, col - 1

        # create and update event
        try:
            player_name = manager.get_turn_player_name()
            event = PlayerPlacementEvent.create(player_name=player_name, row=row, col=col)
            manager.update(event)
        except Exception as e:
            print(e)
            continue
        else:
            manager.draw()


if __name__ == '__main__':
    main_turn()
