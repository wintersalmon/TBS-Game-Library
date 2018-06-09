from tbs.error import InvalidPositionError
from tbs.event import Event, EventFactory


class PlayerPlacementEvent(Event):
    def __init__(self, row: int, col: int):
        super(PlayerPlacementEvent, self).__init__(row=row, col=col)

    @property
    def row(self):
        return self.get_parameter('row')

    @property
    def col(self):
        return self.get_parameter('col')

    def _update(self, game):
        player_marker = game.status.player
        flip_positions = game.board.find_flip_positions(self.row, self.col, player_marker)

        if len(flip_positions) == 0:
            raise InvalidPositionError(
                'invalid position ({}, {}), has not target to flip'.format(self.row, self.col, player_marker))

        game.board.set(self.row, self.col, player_marker)
        game.status.update(game)

    def _rollback(self, game):
        game.board.reset_tile(self.row, self.col)
        game.status.rollback(game)

    def _validate_update_or_raise_error(self, game):
        return

    def _create_game_backup(self, game):
        return dict()

    def _restore_from_backup(self, game, backup):
        return


class OthelloEventFactory(EventFactory):
    pass


OthelloEventFactory.register(1001, PlayerPlacementEvent)
