from tbs.event import Event, EventFactory


class PlayerPlacementEvent(Event):
    def __init__(self, player: int, row: int, col: int):
        super(PlayerPlacementEvent, self).__init__(player=player, row=row, col=col)

    @property
    def player(self):
        return self.get_parameter('player')

    @property
    def row(self):
        return self.get_parameter('row')

    @property
    def col(self):
        return self.get_parameter('col')

    def _update(self, game):
        game.board.set(self.row, self.col, self.player)
        game.status.update(game)

    def _rollback(self, game):
        game.board.reset_tile(self.row, self.col)
        game.status.rollback(game)

    def _validate_update_or_raise_error(self, game):
        self._validate_value_eq_or_raise_error(
            name='player',
            current=self.player,
            required=game.status.turn_player)

        self._validate_value_eq_or_raise_error(
            name='tile is not occupied',
            current=game.board.is_set(self.row, self.col),
            required=False)

    def _create_game_backup(self, game):
        return {
            'tile': game.board.get(self.row, self.col)
        }

    def _restore_from_backup(self, game, backup):
        game.board.set(self.row, self.col, backup['tile'])


class TTTEventFactory(EventFactory):
    pass


TTTEventFactory.register(1001, PlayerPlacementEvent)
