from tbs.cli import CLIReplay
from mandom.cli.mandom import MandomCLIDraw
from mandom.managers import MandomReplayManager


class GameApp(CLIReplay):
    def __init__(self):
        super().__init__(cls_manager=MandomReplayManager)

    def draw(self):
        self._draw_game_replay_status()
        MandomCLIDraw.draw(self.manager.wrapper.game)
