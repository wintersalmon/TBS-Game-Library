from chess.piece import ChessPiece
from tbs.error import ApiEventError
from tbs.event import SimpleRollbackEvent, EventFactory
from tbs.position import Position


class MoveChessPieceEvent(SimpleRollbackEvent):
    def _update(self, game):
        piece_src = game.board.get(*self.pos_src)
        game.board.set(*self.pos_dst, piece_src)
        game.board.reset_tile(*self.pos_src)

    def _validate_update_or_raise_error(self, game):
        piece_src = game.board.get(*self.pos_src)
        if isinstance(piece_src, ChessPiece) and piece_src.is_valid_destination(game.board, self.pos_src, self.pos_dst):
            return
        raise ApiEventError('invalid move positions')

    def _create_game_backup(self, game):
        return {
            'piece_src': game.board.get(*self.pos_src),
            'piece_dst': game.board.get(*self.pos_dst),
        }

    def _restore_from_backup(self, game, backup):
        game.board.set(*self.pos_src, backup['piece_src'])
        game.board.set(*self.pos_dst, backup['piece_dst'])

    @property
    def pos_src(self):
        return self.get_parameter('pos_src')

    @property
    def pos_dst(self):
        return self.get_parameter('pos_dst')

    def encode(self):
        return {
            'pos_src': self.pos_src.encode(),
            'pos_dst': self.pos_dst.encode(),
        }

    @classmethod
    def decode(cls, **kwargs):
        pos_src = Position.decode(**kwargs['pos_src'])
        pos_dst = Position.decode(**kwargs['pos_dst'])
        return cls(pos_src=pos_src, pos_dst=pos_dst)


class ChessEventFactory(EventFactory):
    pass


ChessEventFactory.register(1001, MoveChessPieceEvent)
