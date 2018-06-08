from mandom.data.status import StatusCode
from tbs.event import SimpleRollbackEvent


class ChallengeDungeonEvent(SimpleRollbackEvent):

    def __init__(self, player):
        super(ChallengeDungeonEvent, self).__init__(player=player)

    @property
    def player(self):
        return self.get_parameter('player')

    def _update(self, game):
        battle_result = game.dungeon.challenge(game.hero)

        if battle_result > 0:
            game.players[self.player].victory_point += 1
        else:
            game.players[self.player].life_point -= 1

        if game.players[self.player].victory_point >= 2:
            game.status = StatusCode.GAME_OVER
        else:
            game.status = StatusCode.CHALLENGE

    def _validate_update_or_raise_error(self, game):
        self._validate_value_eq_or_raise_error(
            name='status',
            current=game.status,
            required=StatusCode.ROUND)

        self._validate_value_eq_or_raise_error(
            name='player',
            current=game.player_turn_tracker.current_player,
            required=self.player)

        self._validate_value_eq_or_raise_error(
            name='active player count',
            current=len(game.player_turn_tracker),
            required=1,
        )

    def _create_game_backup(self, game):
        backup_data = dict()
        backup_data['turn_player_life_point'] = game.players[self.player].life_point
        backup_data['turn_player_victory_point'] = game.players[self.player].victory_point
        backup_data['status'] = game.status
        return backup_data

    def _restore_from_backup(self, game, backup):
        game.players[self.player].life_point = backup['turn_player_life_point']
        game.players[self.player].victory_point = backup['turn_player_victory_point']
        game.status = backup['status']
