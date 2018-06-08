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
        self._is_update_applied = False

    def get_parameter(self, key):
        return self._params[key]

    def update(self, game):
        if self._is_update_applied:
            raise ApiEventError('invalid action update')

        self._validate_update_or_raise_error(game)

        temp_backup = self._create_game_backup(game)
        try:
            self._update(game)
        except Exception as e:
            self._restore_from_backup(game, temp_backup)
            raise
        else:
            self._is_update_applied = True
        return temp_backup

    def rollback(self, game):
        if not self._is_update_applied:
            raise ApiEventError('invalid action rollback')

        temp_backup = self._create_game_backup(game)
        try:
            self._rollback(game)
        except Exception as e:
            self._restore_from_backup(game, temp_backup)
            raise
        else:
            self._is_update_applied = False
        return temp_backup

    def _update(self, game):
        raise NotImplementedError

    def _rollback(self, game):
        raise NotImplementedError

    def _validate_update_or_raise_error(self, game):
        raise NotImplementedError

    def _create_game_backup(self, game):
        raise NotImplementedError

    def _restore_from_backup(self, game, backup):
        raise NotImplementedError

    @classmethod
    def _validate_value_in_or_raise_error(cls, name, current, required):
        if current in required:
            return
        raise ApiEventError(cls._create_value_error_fmt(name, current, 'in', required))

    @classmethod
    def _validate_value_eq_or_raise_error(cls, name, current, required):
        if current == required:
            return
        raise ApiEventError(cls._create_value_error_fmt(name, current, '==', required))

    @classmethod
    def _validate_value_gt_or_raise_error(cls, name, current, required):
        if current > required:
            return
        raise ApiEventError(cls._create_value_error_fmt(name, current, '>', required))

    @classmethod
    def _create_value_error_fmt(cls, name, current, operator, required):
        return 'invalid value {name}: {cur} {op} {req}'.format(
            name=name,
            cur=current,
            op=operator,
            req=required)

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

    def _validate_update_or_raise_error(self, game):
        raise NotImplementedError

    def _create_game_backup(self, game):
        raise NotImplementedError

    def _restore_from_backup(self, game, backup):
        raise NotImplementedError
