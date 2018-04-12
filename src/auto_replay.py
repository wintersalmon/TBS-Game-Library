import getopt
import importlib
import sys


def show_usage_and_exit(code: int, error_msg: str = None):
    if error_msg:
        print(error_msg)
    print("main.py <package> <file_name>")
    print("option (-s --simple): simple output")
    print("option (-w --wait): wait time after each cycle (w >= 0)")
    sys.exit(code)


def main():
    package_name = ''
    load_file_name = ''
    wait_time = 0
    simple_output_mode = False

    try:
        opts, args = getopt.getopt(sys.argv[1:], "w:hs", ["help", "simple", "wait="])

        for opt, arg in opts:
            if opt in ("-h", "--help"):
                show_usage_and_exit(0)
                sys.exit()
            elif opt in ("-w", "--wait"):
                wait_time = int(arg)
            elif opt in ("-s", "--simple"):
                simple_output_mode = True

        if len(args) == 2:
            package_name = args[0]
            load_file_name = args[1]
        else:
            show_usage_and_exit(3, 'need two arguments')

        if wait_time < 0:
            show_usage_and_exit(2, 'wait time must be positive number')

    except getopt.GetoptError as e:
        show_usage_and_exit(1, str(e))

    # load package
    package = importlib.import_module(package_name)
    cls_ui = getattr(package, 'CLIReplayAuto')

    # run game, if something goes wrong temp save game
    ui = cls_ui(file_name=load_file_name, wait_time=wait_time, simple_output_mode=simple_output_mode)
    ui.run()


if __name__ == '__main__':
    main()
