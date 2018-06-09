import getopt
import importlib
import sys

GAME_UI_CLI = 'cli'
GAME_UI_GUI = 'gui'

GAME_COMMAND_RUN = 'play'
GAME_COMMAND_REPLAY = 'replay'


def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "h", ["help", "cli"])
    except getopt.GetoptError as e:
        show_usage(str(e))
        sys.exit(1)

    game_ui = GAME_UI_GUI
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            show_usage()
            sys.exit()
        elif opt == "--cli":
            game_ui = GAME_UI_CLI

    try:
        game_mode = args[0]
        if game_mode not in (GAME_COMMAND_RUN, GAME_COMMAND_REPLAY):
            show_usage("invalid command {}".format(game_mode))
            sys.exit(2)
        game_name = args[1]

    except IndexError:
        show_usage("invalid arguments")
        sys.exit(3)

    game_module = importlib.import_module('{}.{}.{}'.format(game_name, game_ui, game_mode))
    app = getattr(game_module, 'GameApp')
    app().run()


def show_usage(error_msg=None):
    if error_msg:
        print(error_msg)
    print("main.py play <package> [--cli]    # create new game")
    print("main.py replay <package> [--cli]  # load saved game in replay mode")
    print("    --cli: load game in CLI(command line interface) mode")


if __name__ == '__main__':
    main()
