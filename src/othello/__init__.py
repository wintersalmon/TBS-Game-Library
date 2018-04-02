from .main import main_loop, replay_loop
from .wrapper import OthelloWrapper as Wrapper
from .wrapper import OthelloCLIWrapper as CLIWrapper

__all__ = [
    'main_loop',
    'replay_loop',
    'Wrapper',
    'CLIWrapper',
]
