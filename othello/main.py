from board import InvalidPositionError
from events import PlayerPlacementEvent
from othello import Othello


def main():
    othello = Othello(player_one='tom', player_two='jerry')

    while othello:
        draw(othello)
        try:
            row, col = get_user_input_or_raise_error()
            event = PlayerPlacementEvent.create(row=row, col=col)
            event.update(othello)
        except EOFError as e:
            print(e)
            exit()
        except InvalidPositionError as e:
            print(e.__class__.__name__, e)
        except ValueError as e:
            print(e)


def get_user_input_or_raise_error():
    row, col = input('row, col: ').split()
    row, col = int(row), int(col)

    if row == 0 and col == 0:
        raise EOFError

    row, col = row - 1, col - 1

    return row, col


def draw(game):
    markers = [' ', '○', '●']
    for row in range(game.board.rows):
        for col in range(game.board.cols):
            idx = game.board.tiles[row][col]
            print('[{}]'.format(markers[idx]), end='')
        print()
    print()


if __name__ == '__main__':
    main()
