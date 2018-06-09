from mandom.data.player import PlayerTurnTracker
from mandom.data.status import StatusCode
from tbs.event import Event


class TurnFoldEvent(Event):
    def __init__(self, player: int):
        super(TurnFoldEvent, self).__init__(player=player)

    @property
    def player(self):
        return self.get_parameter('player')

    def _update(self, game):
        game.player_turn_tracker.update_turn_forward_and_disable_player()

    def _rollback(self, game):
        game.player_turn_tracker.update_turn_backward_and_enable_player()

    def _validate_update_or_raise_error(self, game):
        self._validate_value_eq_or_raise_error(
            name='status',
            current=game.status,
            required=StatusCode.ROUND)

        self._validate_value_eq_or_raise_error(
            name='player',
            current=game.player_turn_tracker.current_player,
            required=self.player)

        self._validate_value_gt_or_raise_error(
            name='active player count',
            current=len(game.player_turn_tracker),
            required=1,
        )

    def _create_game_backup(self, game):
        backup = dict()
        backup['player_turn_tracker'] = game.player_turn_tracker.encode()
        return backup

    def _restore_from_backup(self, game, backup):
        game.player_turn_tracker = PlayerTurnTracker.decode(**backup['player_turn_tracker'])
