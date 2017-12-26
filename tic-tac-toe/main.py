from events.placement_event import PlayerPlacementEvent
from tic_tac_toe import TicTacToe
from tic_tac_toe_manager import TicTacToeManager


def main_auto():
    names = ('tom', 'jerry')
    game = TicTacToe(player_one=names[0], player_two=names[1], rows=3, cols=3)

    events = list()
    turn = 0
    for row in range(game.board.rows):
        for col in range(game.board.cols):
            name = names[turn % 2]
            event = PlayerPlacementEvent.create(game, name=name, row=row, col=col)
            event.update(game)

            print(event)
            print(game)

            events.append(event)
            turn += 1
    print(events)


def main_turn():
    names = ('tom', 'jerry')
    manager = TicTacToeManager(player_one=names[0], player_two=names[1], rows=3, cols=3)

    events = list()
    turn = 0
    while turn < (manager.game.board.rows * manager.game.board.cols):
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

        try:
            name = names[turn % 2]
            event = PlayerPlacementEvent.create(manager.game, name=name, row=row, col=col)
            manager.update(event)

        except ValueError as e:
            print(e)

        else:
            manager.draw()
            turn += 1

        # check victory condition
        if manager.game.board.has_bingo():
            break

    print(events)


if __name__ == '__main__':
    # main_auto()
    main_turn()
