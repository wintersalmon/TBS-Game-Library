from mandom.data.deck import Deck
from mandom.data.dungeon import Dungeon
from mandom.data.player import PlayerTurnTracker
from mandom.data.status import StatusCode
from tbs.event import Event


class TurnAddMonsterToDungeon(Event):
    def __init__(self, player: int):
        super(TurnAddMonsterToDungeon, self).__init__(player=player)

    @property
    def player(self):
        return self.get_parameter('player')

    def _update(self, game):
        card = game.deck.draw()
        game.dungeon.push(card)
        game.player_turn_tracker.update_turn_forward()
        game.status = StatusCode.ROUND

    def _rollback(self, game):
        card = game.dungeon.pop()
        game.deck.return_to_top(card)
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
            name='active player count',
            current=len(game.deck),
            required=0,
        )

    def _create_game_backup(self, game):
        backup_data = dict()
        backup_data['deck'] = game.deck.encode()
        backup_data['dungeon'] = game.dungeon.encode()
        backup_data['player_turn_tracker'] = game.player_turn_tracker.encode()
        backup_data['status'] = game.status
        return backup_data

    def _restore_from_backup(self, game, backup):
        game.deck = Deck.decode(**backup['deck'])
        game.dungeon = Dungeon.decode(**backup['dungeon'])
        game.player_turn_tracker = PlayerTurnTracker.decode(**backup['player_turn_tracker'])
        game.status = backup['status']
