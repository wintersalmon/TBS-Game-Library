import getopt
import importlib
import sys

GAME_UI_CLI = 'cli'
GAME_UI_GUI = 'gui'

GAME_COMMAND_RUN = 'run'
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
        command = args[0]
        if command == GAME_COMMAND_RUN:
            game_mode = 'play'
        elif command == GAME_COMMAND_REPLAY:
            game_mode = 'replay'
        else:
            show_usage("invalid command {}".format(command))
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
    print("main.py run <package>    # run game")
    print("main.py replay <package> # load game replay")
    print("main.py --cli run <package>    # run game in cli mode")
    print("main.py --cli replay <package> # load game replay in cli mode")


if __name__ == '__main__':
    main()
