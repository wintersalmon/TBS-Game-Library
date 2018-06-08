from tbs.error import ApiEventError
from tbs.utils import SerializableMixin


# from tbs.error import InvalidParameterError
# from tbs.utils import SerializableMixin
#
#
# class Event(SerializableMixin):
#     def update(self, game):
#         raise NotImplementedError
#
#     def rollback(self, game):
#         raise NotImplementedError
#
#     def encode(self):
#         raise NotImplementedError
#
#     @classmethod
#     def decode(cls, **kwargs):
#         raise NotImplementedError
#
#     @classmethod
#     def create(cls, *, game, **kwargs):
#         raise NotImplementedError
#
#     @classmethod
#     def get_argument_or_raise_error(cls, kwargs, key):
#         try:
#             value = kwargs[key]
#         except KeyError:
#             raise InvalidParameterError('missing parameter: ' + key)
#         else:
#             return value
#
#     def __str__(self):
#         return '{}{}'.format(self.__class__.__name__, tuple(self.__dict__.values()))


class Event(SerializableMixin):
    def __init__(self, **kwargs):
        super().__init__()
        self._params = kwargs
        self._can_apply_update = True

    def get_parameter(self, key):
        return self._params[key]

    @property
    def can_apply_update(self):
        return self._can_apply_update

    @property
    def can_apply_rollback(self):
        return not self._can_apply_update

    def update(self, game):
        if not self.can_apply_update:
            raise ApiEventError('cannot update event')

        if not self._event_update_valid(game):
            raise ApiEventError('event is not valid')

        temp_backup = self._create_game_backup(game)

        try:
            self._update(game)
        except Exception as e:
            self._restore_from_backup(game, temp_backup)
            raise
        else:
            self._can_apply_update = False
        return temp_backup

    def rollback(self, game):
        if not self.can_apply_rollback:
            raise ApiEventError('cannot rollback event')

        temp_backup = self._create_game_backup(game)

        try:
            self._rollback(game)
        except Exception as e:
            self._restore_from_backup(game, temp_backup)
            raise
        else:
            self._can_apply_update = True

    def _update(self, game):
        raise NotImplementedError

    def _rollback(self, game):
        raise NotImplementedError

    def _event_update_valid(self, game):
        raise NotImplementedError

    def _create_game_backup(self, game):
        raise NotImplementedError

    def _restore_from_backup(self, game, backup):
        raise NotImplementedError

    def encode(self):
        return self._params

    @classmethod
    def decode(cls, **kwargs):
        return cls(**kwargs)

    def __str__(self):
        return '{}({})'.format(self.__class__.__name__, self._params)


class SimpleRollbackEvent(Event):
    def __init__(self, **kwargs):
        super(SimpleRollbackEvent, self).__init__(**kwargs)
        self._update_backup = None

    def update(self, game):
        self._update_backup = super().update(game)

    def _rollback(self, game):
        self._restore_from_backup(game, self._update_backup)

    def _update(self, game):
        raise NotImplementedError

    def _event_update_valid(self, game):
        raise NotImplementedError

    def _create_game_backup(self, game):
        raise NotImplementedError

    def _restore_from_backup(self, game, backup):
        raise NotImplementedError
