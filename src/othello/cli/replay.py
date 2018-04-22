from core.cli import CLIReplay
from othello.managers import OthelloReplayManager
from .draw import OthelloCLIDrawMixin


class OthelloCLIReplay(CLIReplay, OthelloCLIDrawMixin):
    def __init__(self):
        super().__init__(cls_manager=OthelloReplayManager)

    def draw(self):
        super().draw()
        game = self.manager.wrapper.game
        self.draw_status(game)
        self.draw_board(game)


GameApp = OthelloCLIReplay

# class OthelloCLIAutoReplay(OthelloCLIReplay):
#     def __init__(self, file_name, wait_time=0, simple_output_mode=False):
#         super().__init__(file_name=file_name)
#         self.wait_time = wait_time
#         self.simple_output_mode = simple_output_mode
#
#     def draw(self):
#         if self.simple_output_mode:
#             self.draw_status(self.manager.wrapper.game)
#         else:
#             super().draw()
#
#     def clean(self):
#         self.manager = None
#
#     def update(self):
#         self.manager.forward()
#         if self.wait_time:
#             time.sleep(self.wait_time)
#
#     def status(self):
#         return super().status() and self.manager.get_position() < self.manager.get_max_position()
