from chess.events import MoveChessPieceEvent
from chess.managers import ChessUpdateManager, ChessReplayManager
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


def replay_main():
    settings = {
        'player_names': ['tom', 'jerry']
    }
    chess_wrapper = ChessWrapper.create(**settings)
    chess_update_manager = ChessUpdateManager(chess_wrapper)

    event = MoveChessPieceEvent.create(game=chess_wrapper.game,
                                       pos_src=Position(row=1, col=0),
                                       pos_dst=Position(row=3, col=0))
    chess_update_manager.update(event)
    print(chess_update_manager)

    event = MoveChessPieceEvent.create(game=chess_wrapper.game,
                                       pos_src=Position(row=6, col=0),
                                       pos_dst=Position(row=4, col=0))
    chess_update_manager.update(event)
    print(chess_update_manager)

    event = MoveChessPieceEvent.create(game=chess_wrapper.game,
                                       pos_src=Position(row=1, col=1),
                                       pos_dst=Position(row=2, col=1))
    chess_update_manager.update(event)
    print(chess_update_manager)

    event = MoveChessPieceEvent.create(game=chess_wrapper.game,
                                       pos_src=Position(row=6, col=1),
                                       pos_dst=Position(row=4, col=1))
    chess_update_manager.update(event)
    print(chess_update_manager)

    event = MoveChessPieceEvent.create(game=chess_wrapper.game,
                                       pos_src=Position(row=3, col=0),
                                       pos_dst=Position(row=4, col=1))
    chess_update_manager.update(event)
    print(chess_update_manager)

    event = MoveChessPieceEvent.create(game=chess_wrapper.game,
                                       pos_src=Position(row=0, col=0),
                                       pos_dst=Position(row=4, col=0))
    chess_update_manager.update(event)
    print(chess_update_manager)

    print(chess_update_manager)
    encoded_game_data = chess_wrapper.encode()

    print('INIT')
    chess_wrapper = ChessWrapper.decode(**encoded_game_data)
    replay_manger = ChessReplayManager(chess_wrapper)
    print(replay_manger)

    print('BACKWARD')
    while replay_manger.get_position() > 0:
        replay_manger.backward()
        print(replay_manger)

    print('FORWARD')
    while replay_manger.get_position() < replay_manger.get_max_position():
        replay_manger.forward()
        print(replay_manger)

    print('SET 0')
    replay_manger.set_position(0)
    print(replay_manger)

    print('SET 4')
    replay_manger.set_position(4)
    print(replay_manger)

    print('SET 1')
    replay_manger.set_position(1)
    print(replay_manger)

    print('SET MAX')
    replay_manger.set_position(replay_manger.get_max_position())
    print(replay_manger)

    # board = replay_manger.game_wrapper.game.board
    # for row in range(8):
    #     for col in range(8):
    #         piece = board.get(row, col)
    #         if isinstance(piece, ChessPiece):
    #             print(row, col, piece.name, piece.search_valid_destinations(board, src=Position(row, col)), sep='\t')


if __name__ == '__main__':
    main()
