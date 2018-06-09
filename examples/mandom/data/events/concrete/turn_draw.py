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
        backup['status'] = game.status
        return backup

    def _restore_from_backup(self, game, backup):
        game.status = backup['status']
