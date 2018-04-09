import getopt
import sys

from datetime import datetime

from core.error import ApiError
from othello.ui import OthelloCLIAutoPlay


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

    if len(args) == 1:
        load_file_name = None
    elif len(args) == 2:
        load_file_name = args[1]
    else:
        show_usage("must have 1 or 2 arguments")
        sys.exit(3)

    # run game, if something goes wrong temp save game
    # ui = OthelloCLIAutoPlay(file_name=load_file_name, is_simple_draw=False)
    ui = OthelloCLIAutoPlay(file_name=load_file_name, wait_time=1, is_simple_draw=False)
    # ui = OthelloCLIAutoPlay(file_name=load_file_name)
    try:
        ui.run()
    except ApiError as e:
        print('unexpected error: ', e)
        ui.save_as('dump_{}'.format(datetime.now().strftime('%Y_%m_%d_%H_%M_%S')))
    except Exception as e:
        print('unexpected error: ', e)
        ui.save_as('dump_{}'.format(datetime.now().strftime('%Y_%m_%d_%H_%M_%S')))


if __name__ == '__main__':
    main()
