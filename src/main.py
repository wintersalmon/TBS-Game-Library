import importlib
import sys

if __name__ == '__main__':
    args = list(sys.argv)

    if len(args) in (2, 3):
        module_name = args[1]
        mode_name = args[2] if len(args) == 3 else 'main'

        module = importlib.import_module(module_name)
        mode = getattr(module, mode_name)

        mode()

    else:
        print('main.py <package> [mode]')
