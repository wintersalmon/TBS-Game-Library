from mandom.config import APP_SAVE_DIR
from mandom.wrapper import MandomWrapper
from tbs.managers import ReplayManager, UpdateManager


class MandomReplayManager(ReplayManager):
    cls_wrapper = MandomWrapper
    base_save_dir = APP_SAVE_DIR

    def __init__(self, wrapper):
        super(ReplayManager, self).__init__(wrapper=wrapper)
        self._max_position = len(self.wrapper.events)
        self._cur_position = 0

    def set_position(self, position):
        if 0 <= position <= self._max_position:
            pos_difference = position - self._cur_position
            pos_offset = abs(pos_difference)

            if pos_difference >= 0:
                move_to_direction = self.forward
            else:
                move_to_direction = self.backward

            while pos_offset > 0 and move_to_direction():
                pos_offset -= 1

        return self._cur_position == position

    def get_max_position(self):
        return self._max_position

    def get_position(self):
        return self._cur_position

    def forward(self):
        if self._cur_position >= self._max_position:
            return False

        try:
            event = self.wrapper.events[self._cur_position]
            event.update(self.wrapper.game)
        except Exception as e:
            print(e)
            return False
        else:
            self._cur_position += 1
            return True

    def backward(self):
        if self._cur_position < 0:
            return False
        try:
            event = self.wrapper.events[self._cur_position - 1]
            event.rollback(self.wrapper.game)
        except Exception as e:
            print(e)
            return False
        else:
            self._cur_position -= 1
            return True


class MandomUpdateManager(UpdateManager):
    cls_wrapper = MandomWrapper
    base_save_dir = APP_SAVE_DIR

    def update(self, event):
        try:
            event.update(self.wrapper.game)
        except Exception as e:
            raise
        else:
            self.wrapper.events.append(event)
