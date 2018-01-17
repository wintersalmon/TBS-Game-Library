from core.error import ApiError


class ChessApiError(ApiError):
    pass


class ExitGameError(ChessApiError):
    pass


class InvalidInputError(ChessApiError):
    pass


class EventCreationFailed(ChessApiError):
    pass


class InvalidPositionError(ChessApiError):
    pass


class PositionOutOfBoundError(InvalidPositionError):
    pass


class PositionEmptyError(InvalidPositionError):
    pass


class PositionAlreadyOccupiedError(InvalidPositionError):
    pass


class PositionCannotBeReachedError(InvalidPositionError):
    pass
