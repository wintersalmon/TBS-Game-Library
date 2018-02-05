import json
import os
from unittest import TestCase, main

from chess.events import MoveChessPieceEvent
from chess.managers import ChessUpdateManager
from chess.wrapper import ChessWrapper
from core.position import Position
from settings import FT_SCRIPT_DIR


class ChessFunctionalTestCase(TestCase):
    @staticmethod
    def load_json(file_name):
        load_file_name = os.path.join(FT_SCRIPT_DIR, 'chess', file_name)

        with open(load_file_name, 'r', encoding='utf-8') as infile:
            return json.load(infile)

    def test_basic_game(self):
        settings = {
            'player_names': ['alpha', 'beta']
        }
        chess_wrapper = ChessWrapper.create(**settings)
        chess_update_manager = ChessUpdateManager(chess_wrapper)
        # print(chess_update_manager)

        event = MoveChessPieceEvent.create(game=chess_wrapper.game,
                                           pos_src=Position(row=1, col=0),
                                           pos_dst=Position(row=3, col=0))
        chess_update_manager.update(event)
        # print(chess_update_manager)

        event = MoveChessPieceEvent.create(game=chess_wrapper.game,
                                           pos_src=Position(row=6, col=0),
                                           pos_dst=Position(row=4, col=0))
        chess_update_manager.update(event)
        # print(chess_update_manager)

        event = MoveChessPieceEvent.create(game=chess_wrapper.game,
                                           pos_src=Position(row=1, col=1),
                                           pos_dst=Position(row=2, col=1))
        chess_update_manager.update(event)
        # print(chess_update_manager)

        event = MoveChessPieceEvent.create(game=chess_wrapper.game,
                                           pos_src=Position(row=6, col=1),
                                           pos_dst=Position(row=4, col=1))
        chess_update_manager.update(event)
        # print(chess_update_manager)

        event = MoveChessPieceEvent.create(game=chess_wrapper.game,
                                           pos_src=Position(row=3, col=0),
                                           pos_dst=Position(row=4, col=1))
        chess_update_manager.update(event)
        # print(chess_update_manager)

        event = MoveChessPieceEvent.create(game=chess_wrapper.game,
                                           pos_src=Position(row=0, col=0),
                                           pos_dst=Position(row=4, col=0))
        chess_update_manager.update(event)
        # print(chess_update_manager)

    def test_basic_game_load(self):
        encoded_game = self.load_json('ft_chess_01.json')
        encoded_settings = encoded_game['settings']
        encoded_events = encoded_game['events']
        decoded_game = ChessWrapper.decode(**encoded_game)

        chess_wrapper = ChessWrapper.create(**encoded_settings)
        chess_update_manager = ChessUpdateManager(chess_wrapper)

        events = [MoveChessPieceEvent.decode(**e_data) for e_data in encoded_events]
        for event in events:
            chess_update_manager.update(event)

        for r in range(8):
            for c in range(8):
                src = chess_wrapper.game.board.tiles[r][c]
                dst = decoded_game.game.board.tiles[r][c]
                self.assertEqual(src, dst, msg='({},{}) position does not match'.format(r, c, src, dst))


if __name__ == "__main__":
    main()
