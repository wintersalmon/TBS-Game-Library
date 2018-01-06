from othello.errors import InvalidPositionError, InvalidUserInputError, EndOfInputError
from othello.event import PlayerPlacementEvent
from othello.manager import OthelloManager


def main():
    othello = OthelloManager.create(player_one='tom', player_two='jerry')

    while othello:
        draw(othello.game)
        try:
            row, col = get_user_input_or_raise_error()
            player_num = othello.game.get_turn_player_number()
            event = PlayerPlacementEvent.create(row=row, col=col, player=player_num)
            othello.update(event)

        except InvalidUserInputError as e:
            print(e.__class__.__name__, e)

        except InvalidPositionError as e:
            print(e.__class__.__name__, e)

        except EndOfInputError:
            print('End of Input, Exit game ...')
            break

    en = othello.encode()
    de = OthelloManager.decode(**en)
    draw(de.game)


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
