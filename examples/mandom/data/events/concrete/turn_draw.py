from mandom.data.status import StatusCode
from tbs.event import Event


class TurnDrawEvent(Event):
    def __init__(self, player: int):
        super(TurnDrawEvent, self).__init__(player=player)

    @property
    def player(self):
        return self.get_parameter('player')

    def _update(self, game):
        game.status = StatusCode.TURN

    def _rollback(self, game):
        game.status = StatusCode.ROUND

    def _event_update_valid(self, game):
        if game.status != StatusCode.ROUND:
            return False

        if self.player != game.player_turn_tracker.current_player:
            return False

        if len(game.player_turn_tracker) <= 1:
            return False

        return True

    def _create_game_backup(self, game):
        backup = dict()
        backup['status'] = game.status
        return backup

    def _restore_from_backup(self, game, backup):
        game.status = backup['status']
