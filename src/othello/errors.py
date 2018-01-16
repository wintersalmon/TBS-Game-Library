from core.error import ApiError


class OthelloApiError(ApiError):
    pass


class EndOfInputError(OthelloApiError):
    pass


class InvalidUserInputError(OthelloApiError):
    pass


class InvalidMarkerTypeError(OthelloApiError):
    pass


class InvalidPositionError(OthelloApiError):
    pass


class PositionOutOfBoundsError(InvalidPositionError):
    pass


class PositionAlreadyOccupiedError(InvalidPositionError):
    pass


class PositionHasNoFlipTargetsError(InvalidPositionError):
    pass
