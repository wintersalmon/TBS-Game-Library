from errors import InvalidPositionError, InvalidUserInputError, EndOfInputError
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

        except InvalidUserInputError as e:
            print(e.__class__.__name__, e)

        except InvalidPositionError as e:
            print(e.__class__.__name__, e)

        except EndOfInputError:
            print('End of Input, Exit game ...')
            exit()


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


def draw(game):
    markers = [' ', '●', '○']
    for row in range(game.board.rows):
        for col in range(game.board.cols):
            idx = game.board.tiles[row][col]
            print('[{}]'.format(markers[idx]), end='')
        print()
    print()


if __name__ == '__main__':
    main()
