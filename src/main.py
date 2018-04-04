import getopt
import importlib
import sys

from core.error import ApiError


def show_usage(error_msg=None):
    if error_msg:
        print(error_msg)
    print("main.py <package>  # create new game")
    print("main.py <package> <file_name>  # load existing game with <file_name>")
    print("main.py -r <package> <file_name>  # load existing game in replay mode")


def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hrg", ["help", "replay", "gui"])
    except getopt.GetoptError as e:
        show_usage(str(e))
        sys.exit(1)

    # determine game UI and MODE from given options
    game_ui = 'CLI'
    game_mode = 'Play'
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            show_usage()
            sys.exit()
        elif opt in ("-r", "--replay"):
            game_mode = 'Replay'
        elif opt in ("-g", "--gui"):
            game_ui = 'GUI'

    # determine game PACKAGE and FILE from given arguments
    package_name = args[0]
    if len(args) == 1:
        load_file_name = None
    elif len(args) == 2:
        load_file_name = args[1]
    else:
        show_usage("must have 1 or 2 arguments")
        sys.exit(3)

    # load package
    package = importlib.import_module(package_name)
    ui_name = game_ui + game_mode
    cls_ui = getattr(package, ui_name)

    # run game, if something goes wrong temp save game
    save_game_temp = False
    ui = cls_ui(file_name=load_file_name)
    try:
        ui.run()
    except ApiError as e:
        print('unexpected error: ', e)
        save_game_temp = True

    if hasattr(ui, 'save'):
        if save_game_temp:
            ui.save(save_as=load_file_name + '.temp')
        else:
            ui.save()


if __name__ == '__main__':
    main()
