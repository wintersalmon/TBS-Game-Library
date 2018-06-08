import random
from datetime import datetime

from mandom.data.deck import Deck
from mandom.data.dungeon import Dungeon
from mandom.data.hero import Hero
from mandom.data.monsters import MonsterStack
from mandom.data.player import PlayerTurnTracker
from mandom.data.status import StatusCode
from mandom.data.weapons import WeaponStack
from tbs.event import SimpleRollbackEvent

MAX_RANDOM_SEED_VALUE = 622_702_080


class InitRoundEvent(SimpleRollbackEvent):
    def __init__(self, seed_value: int = None):
        if seed_value is None:
            seed_value = random.Random(datetime.now()).randint(1, MAX_RANDOM_SEED_VALUE)
        super(InitRoundEvent, self).__init__(seed_value=seed_value)

    @property
    def seed_value(self):
        return self.get_parameter('seed_value')

    def _update(self, game):
        game.removed_monsters.clear()
        game.removed_weapons.clear()
        game.hero.restore_to_default_equipment()
        game.deck.restore_and_shuffle(self.seed_value)
        game.dungeon.clear()
        if game.status == StatusCode.CHALLENGE:
            players = [p for p, player in enumerate(game.players) if player.life_point > 0]
            starting_player = game.player_turn_tracker.current_player
            game.player_turn_tracker.reset_turn_order(players=players, starting_player=starting_player)

        # update status
        game.status = StatusCode.ROUND

    def _event_update_valid(self, game):
        # check game status
        if game.status in (StatusCode.GAME_INIT, StatusCode.CHALLENGE):
            return True
        else:
            return False

    def _create_game_backup(self, game):
        backup_data = dict()
        backup_data['removed_monsters'] = game.removed_monsters.encode()
        backup_data['removed_weapons'] = game.removed_weapons.encode()
        backup_data['hero'] = game.hero.encode()
        backup_data['deck'] = game.deck.encode()
        backup_data['dungeon'] = game.dungeon.encode()
        backup_data['player_turn_tracker'] = game.player_turn_tracker.encode()
        backup_data['status'] = game.status
        return backup_data

    def _restore_from_backup(self, game, backup):
        game.removed_monsters = MonsterStack.decode(**backup['removed_monsters'])
        game.removed_weapons = WeaponStack.decode(**backup['removed_weapons'])
        game.hero = Hero.decode(**backup['hero'])
        game.deck = Deck.decode(**backup['deck'])
        game.dungeon = Dungeon.decode(**backup['dungeon'])
        game.player_turn_tracker = PlayerTurnTracker.decode(**backup['player_turn_tracker'])
        game.status = backup['status']
