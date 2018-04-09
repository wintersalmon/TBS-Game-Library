from core.error import ExitGameException
from core.managers import ReplayManager, UpdateManager


class UIMixin(object):
    def run(self):
        self.init()
        self.draw()
        try:
            while self.status():
                self.update()
                self.draw()
        except ExitGameException as e:
            print(e)
        self.clean()

    def init(self):
        pass

    def clean(self):
        pass

    def update(self):
        raise NotImplementedError

    def draw(self):
        raise NotImplementedError

    def status(self):
        raise NotImplementedError


class CLIReplay(UIMixin):
    def __init__(self, cls_wrapper, save_dir, file_name):
        super().__init__()
        self.cls_wrapper = cls_wrapper
        self.save_dir = save_dir
        self.file_name = file_name
        self.manager = None

    def init(self):
        self.manager = ReplayManager.load(self.cls_wrapper, self.save_dir, self.file_name)
        self.manager.set_position(0)

    def clean(self):
        self.manager = None

    def update(self):
        command = input('input command (Quit|Next|Prev|Index) :').lower()
        if command in ('quit', 'q'):
            raise ExitGameException
        elif command in ('next', 'n') or len(command) == 0:
            self.manager.forward()
        elif command in ('prev', 'p'):
            self.manager.backward()
        else:
            try:
                index = int(command)
            except ValueError:
                print('invalid command', command)
            else:
                self.manager.set_position(index)

    def status(self):
        return self.manager is not None

    def draw(self):
        print()
        replay_repr = 'Position: {}/{}'.format(self.manager.get_position(), self.manager.get_max_position())
        if self.manager.get_position() == 0:
            prev_event = 'NO_PREV_EVENT'
        else:
            prev_event = str(self.manager.wrapper.events[self.manager.get_position() - 1])

        if self.manager.get_position() == self.manager.get_max_position():
            next_event = 'NO_NEXT_EVENT'
        else:
            next_event = str(self.manager.wrapper.events[self.manager.get_position()])

        print('\n'.join((replay_repr, prev_event, next_event)))


class CLIPlay(UIMixin):
    def __init__(self, cls_wrapper, save_dir, file_name):
        super().__init__()
        self.cls_wrapper = cls_wrapper
        self.save_dir = save_dir
        self.file_name = file_name
        self.manager = None

    def init(self):
        if self.file_name:
            self.manager = UpdateManager.load(self.cls_wrapper, self.save_dir, self.file_name)
        else:
            settings = self._create_game_settings()
            wrapper = self.cls_wrapper.create(**settings)
            self.manager = UpdateManager(wrapper=wrapper)

    def clean(self):
        save_file_name = None

        save_progress = input('save progress? (Y, n) ').lower() or 'y'

        if save_progress == 'y':
            if self.file_name:
                save_file_name = self.file_name
            else:
                save_file_name = input('save file name? (press ENTER to skip) ')

        if save_file_name:
            self.manager.save(self.save_dir, save_file_name)

    def draw(self):
        print()
        event_repr = 'Total Events: {}'.format(len(self.manager.wrapper.events))
        print('\n'.join((event_repr,)))

    def update(self):
        raise NotImplementedError

    def status(self):
        raise NotImplementedError

    def _create_game_settings(self):
        raise NotImplementedError
