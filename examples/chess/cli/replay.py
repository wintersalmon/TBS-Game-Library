from chess.cli.chess import ChessCLIDrawMixin
from chess.managers import ChessReplayManager
from tbs.cli import CLIReplay


class ChessCLIReplay(CLIReplay):
    def __init__(self):
        super().__init__(cls_manager=ChessReplayManager)

    def draw(self):
        super().draw()
        ChessCLIDrawMixin.draw(self.manager.wrapper.game)


GameApp = ChessCLIReplay
