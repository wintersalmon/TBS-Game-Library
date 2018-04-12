from .cli.play import OthelloCLIAutoPlay as CLIPlayAuto
from .cli.play import OthelloCLIPlay as CLIPlay
from .cli.replay import OthelloCLIAutoReplay as CLIReplayAuto
from .cli.replay import OthelloCLIReplay as CLIReplay
from .wrapper import OthelloWrapper as Wrapper

__all__ = [
    'CLIPlayAuto',
    'CLIReplayAuto',
    'CLIPlay',
    'CLIReplay',
    'Wrapper',
]
