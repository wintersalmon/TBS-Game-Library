class ApiException(Exception):
    def __str__(self):
        return '{}({})'.format(self.__class__.__name__, super().__str__())


class ExitGameException(ApiException):
    pass


class ApiError(ApiException):
    pass


class ApiEventError(ApiError):
    pass


class InvalidInputError(ApiError):
    pass


class InvalidPositionError(ApiError):
    pass


class InvalidValueError(ApiError):
    pass


class InvalidParameterError(ApiError):
    pass


class EventCreationFailedError(ApiError):
    pass


class PositionOutOfBoundError(InvalidPositionError):
    pass


class PositionAlreadySetError(InvalidPositionError):
    pass
