from mandom.data.deck import Deck
from mandom.data.hero import Hero
from mandom.data.monsters import MonsterStack
from mandom.data.player import PlayerTurnTracker
from mandom.data.status import StatusCode
from mandom.data.weapons import WeaponStack
from mandom.data.weapons.code import WeaponCode
from tbs.event import Event


class TurnRemoveWeaponFromHero(Event):
    def __init__(self, player: int, weapon: int):
        super(TurnRemoveWeaponFromHero, self).__init__(player=player, weapon=weapon)

    @property
    def player(self):
        return self.get_parameter('player')

    @property
    def weapon(self):
        return self.get_parameter('weapon')

    def _update(self, game):
        weapon = WeaponCode(self.weapon)
        monster = game.deck.draw()
        game.hero.disable_weapon(weapon)
        game.removed_weapons.push(weapon)
        game.removed_monsters.push(monster)
        game.player_turn_tracker.update_turn_forward()
        game.status = StatusCode.ROUND

    def _rollback(self, game):
        weapon = game.removed_weapons.pop()
        monster = game.removed_monsters.pop()
        game.hero.enable_weapon(weapon)
        game.deck.return_to_top(monster)
        game.player_turn_tracker.update_turn_backward()
        game.status = StatusCode.TURN

    def _validate_update_or_raise_error(self, game):
        self._validate_value_eq_or_raise_error(
            name='status',
            current=game.status,
            required=StatusCode.TURN)

        self._validate_value_eq_or_raise_error(
            name='player',
            current=game.player_turn_tracker.current_player,
            required=self.player)

        self._validate_value_gt_or_raise_error(
            name='deck size',
            current=len(game.deck),
            required=0,
        )

        self._validate_value_eq_or_raise_error(
            name='weapon active',
            current=WeaponCode(self.weapon) in game.hero.weapons,
            required=True
        )

    def _create_game_backup(self, game):
        backup_data = dict()
        backup_data['removed_monsters'] = game.removed_monsters.encode()
        backup_data['removed_weapons'] = game.removed_weapons.encode()
        backup_data['hero'] = game.hero.encode()
        backup_data['deck'] = game.deck.encode()
        backup_data['player_turn_tracker'] = game.player_turn_tracker.encode()
        backup_data['status'] = game.status
        return backup_data

    def _restore_from_backup(self, game, backup):
        game.removed_monsters = MonsterStack.decode(**backup['removed_monsters'])
        game.removed_weapons = WeaponStack.decode(**backup['removed_weapons'])
        game.hero = Hero.decode(**backup['hero'])
        game.deck = Deck.decode(**backup['deck'])
        game.player_turn_tracker = PlayerTurnTracker.decode(**backup['player_turn_tracker'])
        game.status = backup['status']
