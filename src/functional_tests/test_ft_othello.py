from unittest import main

from functional_tests.base import BaseFunctionalTestCase
from othello.events import PlayerPlacementEvent
from othello.managers import OthelloUpdateManager
from othello.wrapper import OthelloWrapper


class OthelloFunctionalTestCase(BaseFunctionalTestCase):
    def test_basic_game_encode_load_create_compare(self):
        self.maxDiff = None
        self.basic_game_encode_load_create('ft_othello_01.json')
        self.basic_game_encode_load_create('ft_othello_02.json')
        self.basic_game_encode_load_create('ft_othello_03.json')
        self.basic_game_encode_load_create('ft_othello_04.json')
        self.basic_game_encode_load_create('ft_othello_05.json')

    def basic_game_encode_load_create(self, file_name):
        encoded_game = self.load_json('othello', file_name)
        encoded_settings = encoded_game['settings']
        encoded_events = encoded_game['events']
        decoded_game = OthelloWrapper.decode(**encoded_game)

        new_wrapper = OthelloWrapper.create(**encoded_settings)
        new_manager = OthelloUpdateManager(wrapper=new_wrapper)

        self.assertNotEqual(new_manager.wrapper.encode(), decoded_game.encode())

        events = [PlayerPlacementEvent.decode(**e_data) for e_data in encoded_events]
        for event in events:
            new_manager.update(event)

        self.assertEqual(new_manager.wrapper.encode(), decoded_game.encode())
        self.assertEqual(new_manager.wrapper.game.board.count, decoded_game.game.board.count)


if __name__ == "__main__":
    main()
