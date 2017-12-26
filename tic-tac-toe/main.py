from events.placement_event import PlayerPlacementEvent
from tic_tac_toe import TicTacToe


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
    game = TicTacToe(player_one=names[0], player_two=names[1], rows=3, cols=3)

    events = list()
    turn = 0
    while turn < (game.board.rows * game.board.cols):
        try:
            row, col = input('row, col: ').split()
            row, col = int(row), int(col)
            if row == 0 and col == 0:
                exit(0)
            else:
                row, col = row - 1, col - 1
        except ValueError as e:
            print(e)
            continue

        try:
            name = names[turn % 2]
            event = PlayerPlacementEvent.create(game, name=name, row=row, col=col)
            event.update(game)
        except ValueError as e:
            print(e)
        else:
            print(event)
            print(game)
            events.append(event)
            turn += 1

    print(events)


if __name__ == '__main__':
    # main_auto()
    main_turn()
