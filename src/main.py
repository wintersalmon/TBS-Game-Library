import getopt
import importlib
import sys

from core.managers import ReplayManager, UpdateManager
from settings import SAVE_DIR

GAME_MODE_MAIN = 'main'
GAME_MODE_REPLAY = 'replay'


def play_game(update_manager, main_loop):
    print(update_manager)
    while main_loop(update_manager):
        print(update_manager)


def replay_game(manager, replay_loop):
    manager.set_position(0)
    print(manager)
    while replay_loop(manager):
        print(manager)


def load_game(cls_manager, cls_wrapper, file_dir, file_name):
    data = cls_manager.load(file_dir, file_name)
    wrapper = cls_wrapper.decode(**data)
    manager = cls_manager(wrapper=wrapper)
    return manager


def show_usage(error_msg=None):
    if error_msg:
        print(error_msg)
    print("main.py <package>  # create new game")
    print("main.py <package> <file_name>  # load existing game with <file_name>")
    print("main.py -r <package> <file_name>  # load existing game in replay mode")


def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hr", ["help", "replay"])
    except getopt.GetoptError as e:
        show_usage(str(e))
        sys.exit(1)

    if len(opts) > 1:
        show_usage("only one option allowed")
        sys.exit(2)

    package_name = args[0]
    package = importlib.import_module(package_name)
    package_save_dir = SAVE_DIR[package_name]
    wrapper_class = getattr(package, 'CLIWrapper')

    game_mode = GAME_MODE_MAIN
    game_loop = getattr(package, 'main_loop')
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            show_usage()
            sys.exit()
        elif opt in ("-r", "--replay"):
            game_mode = GAME_MODE_REPLAY
            game_loop = getattr(package, 'replay_loop')

    if len(args) == 1:
        save_file_name = None
    elif len(args) == 2:
        save_file_name = args[1]
    else:
        show_usage("must have 1 or 2 arguments")
        sys.exit(3)

    if game_mode == GAME_MODE_REPLAY:
        manager = load_game(ReplayManager, wrapper_class, package_save_dir, save_file_name)
        replay_game(manager=manager, replay_loop=game_loop)
    else:
        if save_file_name:
            manager = load_game(UpdateManager, wrapper_class, package_save_dir, save_file_name)
        else:
            settings = {'player_names': ['tom', 'jerry']}
            wrapper = wrapper_class.create(**settings)
            manager = UpdateManager(wrapper=wrapper)

        play_game(update_manager=manager, main_loop=game_loop)

        save_progress = input('save progress? (YES, no) ').lower()

        if not save_progress or save_progress in ('y', 'yes'):
            if not save_file_name:
                save_file_name = input('save file name? (press ENTER to skip) ')

            if save_file_name:
                manager.save(package_save_dir, save_file_name)


if __name__ == '__main__':
    main()
