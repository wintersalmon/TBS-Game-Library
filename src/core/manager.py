from core.error import CustomError


class GameManager(object):
    def __init__(self, game_wrapper):
        self.game_wrapper = game_wrapper

    def view(self):
        self.game_wrapper.view()


class GameUpdateManager(GameManager):
    def update(self, event):
        try:
            event.update(self.game_wrapper.game)
        except Exception as e:
            raise e
        else:
            self.game_wrapper.events.append(event)


class GameReplayManager(GameManager):
    def __init__(self, game_wrapper):
        super().__init__(game_wrapper=game_wrapper)
        self._max_position = len(self.game_wrapper.events)
        self._cur_position = self._max_position

    def set_position(self, position):
        if 0 <= position <= self._max_position:
            pos_difference = position - self._cur_position
            pos_offset = abs(pos_difference)

            if pos_difference >= 0:
                move_to_direction = self.forward
            else:
                move_to_direction = self.backward

            while pos_offset > 0:
                move_to_direction()
                pos_offset -= 1

    def get_max_position(self):
        return self._max_position

    def get_position(self):
        return self._cur_position

    def forward(self):
        if self._cur_position < self._max_position:
            event = self.game_wrapper.events[self._cur_position]
            event.update(self.game_wrapper.game)
            self._cur_position += 1
            return True
        raise CustomError('Impossible to move forward')

    def backward(self):
        if self._cur_position >= 0:
            event = self.game_wrapper.events[self._cur_position - 1]
            event.rollback(self.game_wrapper.game)
            self._cur_position -= 1
            return True
        raise CustomError('Impossible to move backward')

    def __repr__(self):
        return '{}/{}'.format(self._cur_position, self._max_position)
