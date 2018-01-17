from chess.events import MoveChessPieceEvent
from chess.managers import ChessUpdateManager
from chess.wrapper import ChessWrapper
from core.error import EventCreationFailedError, ExitGameException, InvalidInputError
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
            event = MoveChessPieceEvent.create(game=chess_update_manager.game_wrapper.game,
                                               pos_src=pos_src,
                                               pos_dst=pos_dst)
            chess_update_manager.update(event)
        except ExitGameException as e:
            print(e)
            break
        except InvalidInputError as e:
            print(e)
        except EventCreationFailedError as e:
            print(e)
        else:
            print(chess_update_manager)

    encoded_chess_data = chess_wrapper.encode()
    decoded_chess_data = ChessWrapper.decode(**encoded_chess_data)
    print(decoded_chess_data)


def read_user_event():
    values = input('from(row,col) to(row,col): ').split()

    if len(values) == 0:
        raise ExitGameException('exit game from retrieving empty input')

    try:
        from_row, from_col, to_row, to_col = values
        from_row, from_col, to_row, to_col = int(from_row), int(from_col), int(to_row), int(to_col)
    except ValueError as e:
        raise InvalidInputError('input requires four integers (int>=0): {}'.format(values)) from e
    return Position(row=from_row, col=from_col), Position(row=to_row, col=to_col)


if __name__ == '__main__':
    main()
