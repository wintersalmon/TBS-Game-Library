from .file import FileManager


class ReplayManager(FileManager):
    def __init__(self, wrapper):
        super(ReplayManager, self).__init__(wrapper=wrapper)
        self._max_position = len(self.wrapper.events)
        self._cur_position = self._max_position

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

            return True
        else:
            return False

    def get_max_position(self):
        return self._max_position

    def get_position(self):
        return self._cur_position

    def forward(self):
        if self._cur_position < self._max_position:
            event = self.wrapper.events[self._cur_position]
            event.update(self.wrapper.game)
            self._cur_position += 1
            return True
        else:
            return False

    def backward(self):
        if self._cur_position > 0:
            event = self.wrapper.events[self._cur_position - 1]
            event.rollback(self.wrapper.game)
            self._cur_position -= 1
            return True
        else:
            return False
