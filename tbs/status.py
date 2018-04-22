from tbs.utils import SerializableMixin


class Status(SerializableMixin):
    def __init__(self, code):
        self._code = code

    @property
    def code(self):
        return self._code

    def update(self, game):
        raise NotImplementedError

    def rollback(self, game):
        raise NotImplementedError

    def __bool__(self):
        raise NotImplementedError

    def encode(self):
        return {
            'code': self._code,
        }

    @classmethod
    def decode(cls, **kwargs):
        return cls(**kwargs)


class TurnStatus(Status):
    def __init__(self, code, turn):
        super().__init__(code=code)
        self._turn = turn

    @property
    def turn(self):
        return self._turn

    def update(self, game):
        self._turn += 1

    def rollback(self, game):
        self._turn -= 1

    def __bool__(self):
        raise NotImplementedError

    def encode(self):
        return {
            'code': self._code,
            'turn': self._turn,
        }
