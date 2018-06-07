from mandom.data.events.event import MandomEvent
from mandom.data.player import PlayerTurnTracker
from mandom.data.status import StatusCode


class TurnFoldEvent(MandomEvent):
    def __init__(self, player: int):
        super(TurnFoldEvent, self).__init__(player=player)

    @property
    def player(self):
        return self.get_parameter('player')

    def _update(self, game):
        game.player_turn_tracker.update_turn_forward_and_disable_player()

    def _rollback(self, game):
        game.player_turn_tracker.update_turn_backward_and_enable_player()

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
        backup['player_turn_tracker'] = game.player_turn_tracker.encode()
        return backup

    def _restore_from_backup(self, game, backup):
        game.player_turn_tracker = PlayerTurnTracker.decode(**backup['player_turn_tracker'])
