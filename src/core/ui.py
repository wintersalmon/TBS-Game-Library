from core.managers import ReplayManager, UpdateManager


class UI(object):
    def __init__(self):
        pass

    def run(self):
        raise NotImplementedError


class CLI(UI):
    def __init__(self, file_name):
        super().__init__()
        self.manager = None
        self.file_name = file_name

    def draw(self):
        print(self.manager)

    def run(self):
        raise NotImplementedError


class CLIReplay(CLI):
    def __init__(self, cls_wrapper, save_dir, file_name):
        super().__init__(file_name=file_name)
        self.cls_wrapper = cls_wrapper
        self.save_dir = save_dir

    def run(self):
        self.manager = ReplayManager.load(self.cls_wrapper, self.save_dir, self.file_name)
        self.manager.set_position(0)

        while True:
            self.draw()
            command = input('input command (Quit|Next|Prev|Index) :').lower()
            if command in ('quit', 'q'):
                break
            elif command in ('next', 'n'):
                self.manager.forward()
            elif command in ('prev', 'p'):
                self.manager.backward()
            else:
                try:
                    index = int(command)
                except ValueError as e:
                    print('invalid command', command)
                else:
                    self.manager.set_position(index)


class CLIPlay(CLI):
    def __init__(self, cls_wrapper, save_dir, file_name):
        super().__init__(file_name=file_name)
        self.cls_wrapper = cls_wrapper
        self.save_dir = save_dir

    def run(self):
        if self.file_name:
            self.manager = UpdateManager.load(self.cls_wrapper, self.save_dir, self.file_name)
        else:
            self.manager = self._create_game()

        self.draw()
        while self._main_loop():
            self.draw()

<<<<<<< HEAD
    def _create_game(self):
        raise NotImplementedError

    def _main_loop(self):
        raise NotImplementedError

    def draw(self):
        print(self.manager)

=======
>>>>>>> dev-cli-improvement
    def save(self, *, save_as=None):
        if save_as:
            save_file_name = save_as
        else:
            save_file_name = None

        save_progress = input('save progress? (YES, no) ').lower() or 'yes'

        if save_progress in ('y', 'yes'):
            if self.file_name:
                save_file_name = self.file_name
            else:
                save_file_name = input('save file name? (press ENTER to skip) ')

        if save_file_name:
            self.manager.save(self.save_dir, save_file_name)
<<<<<<< HEAD
=======

    def _create_game(self):
        raise NotImplementedError

    def _main_loop(self):
        raise NotImplementedError
>>>>>>> dev-cli-improvement
