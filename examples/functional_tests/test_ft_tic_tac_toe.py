from unittest import main

from tbs.error import InvalidPositionError
from tbs.managers import UpdateManager
from functional_tests.base import BaseFunctionalTestCase
from tic_tac_toe.data.events import PlayerPlacementEvent
from tic_tac_toe.managers import TicTacToeUpdateManager
from tic_tac_toe.wrapper import TicTacToeWrapper


class TTTFunctionalTestCase(BaseFunctionalTestCase):
    def test_basic_game(self):
        settings = {'player_names': ['tom', 'jerry']}
        manager = TicTacToeUpdateManager.create(**settings)

        event = PlayerPlacementEvent.create(game=manager.wrapper.game, row=1, col=1)
        manager.update(event)
        self.assertEqual(bool(manager.wrapper.game.status), True)

        event = PlayerPlacementEvent.create(game=manager.wrapper.game, row=0, col=0)
        manager.update(event)
        self.assertEqual(bool(manager.wrapper.game.status), True)

        event = PlayerPlacementEvent.create(game=manager.wrapper.game, row=0, col=1)
        manager.update(event)
        self.assertEqual(bool(manager.wrapper.game.status), True)

        event = PlayerPlacementEvent.create(game=manager.wrapper.game, row=0, col=2)
        manager.update(event)
        self.assertEqual(bool(manager.wrapper.game.status), True)

        event = PlayerPlacementEvent.create(game=manager.wrapper.game, row=2, col=1)
        manager.update(event)
        self.assertEqual(bool(manager.wrapper.game.status), False)

    def test_misplacement(self):
        settings = {'player_names': ['tom', 'jerry']}
        wrapper = TicTacToeWrapper.create(**settings)
        manager = UpdateManager(wrapper=wrapper)

        event = PlayerPlacementEvent.create(game=manager.wrapper.game, row=1, col=1)
        manager.update(event)

        event = PlayerPlacementEvent.create(game=manager.wrapper.game, row=1, col=1)
        with self.assertRaises(InvalidPositionError):
            manager.update(event)

        event = PlayerPlacementEvent.create(game=manager.wrapper.game, row=0, col=0)
        manager.update(event)

        event = PlayerPlacementEvent.create(game=manager.wrapper.game, row=1, col=1)
        with self.assertRaises(InvalidPositionError):
            manager.update(event)

        event = PlayerPlacementEvent.create(game=manager.wrapper.game, row=0, col=2)
        manager.update(event)

    def test_basic_game_encode_load_create_compare(self):
        self.run_encode_load_create_from_file('ft_ttt_01.json')
        self.run_encode_load_create_from_file('ft_ttt_02.json')
        self.run_encode_load_create_from_file('ft_ttt_03.json')

    def run_encode_load_create_from_file(self, file_name):
        encoded_game = self.load_json(self.data_dir, file_name)
        encoded_settings = encoded_game['settings']
        encoded_events = encoded_game['events']
        decoded_game = TicTacToeWrapper.decode(**encoded_game)

        new_wrapper = TicTacToeWrapper.create(**encoded_settings)
        new_manager = TicTacToeUpdateManager(wrapper=new_wrapper)

        self.assertNotEqual(new_manager.wrapper.encode(), decoded_game.encode())

        events = [PlayerPlacementEvent.decode(**e_data) for e_data in encoded_events]
        for event in events:
            new_manager.update(event)

        self.assertEqual(new_manager.wrapper.encode(), decoded_game.encode())

    def basic_game_replay(self):
        pass  # todo: write replay test code


if __name__ == "__main__":
    main()
