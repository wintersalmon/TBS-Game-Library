from core.cli import CLIReplay
from tic_tac_toe.cli.tictactoe import TicTacToeCLIDraw
from tic_tac_toe.managers import TicTacToeReplayManager


class GameApp(CLIReplay):
    def __init__(self):
        super().__init__(cls_manager=TicTacToeReplayManager)

    def draw(self):
        self._draw_game_replay_status()
        TicTacToeCLIDraw.draw(self.manager.wrapper.game)
