class OthelloCustomError(Exception):
    pass


class EndOfInputError(OthelloCustomError):
    pass


class InvalidUserInputError(OthelloCustomError):
    pass


class InvalidMarkerTypeError(OthelloCustomError):
    pass


class InvalidPositionError(OthelloCustomError):
    pass


class PositionOutOfBoundsError(InvalidPositionError):
    pass


class PositionAlreadyOccupiedError(InvalidPositionError):
    pass


class PositionHasNoFlipTargetsError(InvalidPositionError):
    pass
