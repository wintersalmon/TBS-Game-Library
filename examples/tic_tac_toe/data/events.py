from tbs.event import Event


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

    # def update(self, game):
    #     if game.board.is_set(self._row, self._col):
    #         raise InvalidPositionError('position already occupied ({},{})'.format(self._row, self._col))
    #
    #     game.board.set(self._row, self._col, self._player)
    #     game.status.update(game)
    #
    # def rollback(self, game):
    #     game.board.reset_tile(self._row, self._col)
    #     game.status.rollback(game)

    # def encode(self):
    #     return {
    #         'player': self._player,
    #         'row': self._row,
    #         'col': self._col,
    #     }
    #
    # @classmethod
    # def decode(cls, **kwargs):
    #     return cls(**kwargs)
    #
    # @classmethod
    # def create(cls, *, game, **kwargs):
    #     row = cls.get_argument_or_raise_error(kwargs, 'row')
    #     col = cls.get_argument_or_raise_error(kwargs, 'col')
    #     player = game.status.turn_player
    #
    #     return cls(player=player, row=row, col=col)
