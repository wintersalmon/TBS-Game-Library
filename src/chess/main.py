from chess.errors import InvalidInputError, ChessApiError, ExitGameError, EventCreationFailed
from chess.events import ChessMovePieceEvent
from chess.managers import ChessUpdateManager
from chess.wrapper import ChessWrapper
from core.position import Position


def main():
    settings = {
        'player_names': ['tom', 'jerry']
    }
    chess_wrapper = ChessWrapper.create(**settings)
    chess_update_manager = ChessUpdateManager(chess_wrapper)

    print(chess_update_manager)
    while chess_update_manager:
        try:
            pos_src, pos_dst = read_user_event()
            event = ChessMovePieceEvent.create(game=chess_update_manager.game_wrapper.game,
                                               pos_src=pos_src,
                                               pos_dst=pos_dst)
            chess_update_manager.update(event)
        except ExitGameError:
            break
        except InvalidInputError as e:
            print(e)
        except EventCreationFailed as e:
            print(e)
        else:
            print(chess_update_manager)

    encoded_chess_data = chess_wrapper.encode()
    decoded_chess_data = ChessWrapper.decode(**encoded_chess_data)
    print(decoded_chess_data)


def read_user_event():
    required_positions = 2
    positions = list()
    for i in range(required_positions):
        try:
            row, col = input('position[{}](row,col): '.format(i)).split()
            row, col = int(row), int(col)

            if row == 0 and col == 0:
                raise ExitGameError

            row, col = row - 1, col - 1
            positions.append(Position(row=row, col=col))
        except ValueError as e:
            raise InvalidInputError('invalid input, requires two integers(int>=0)\nex) (int, int)') from e

    return tuple(positions)


if __name__ == '__main__':
    main()
