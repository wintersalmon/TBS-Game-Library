from core.error import ExitGameException
from core.managers import ReplayManager, UpdateManager


class CLIMixin(object):
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


class CLIReplay(CLIMixin):
    def __init__(self, cls_manager):
        super(CLIReplay, self).__init__()
        if not issubclass(cls_manager, ReplayManager):
            raise NotImplementedError
        self.cls_manager = cls_manager
        self.file_name = None
        self.manager = None

    def init(self):
        self.file_name = input('save file name: ')
        self.manager = self.cls_manager.load(self.file_name)
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
        self._draw_game_replay_status()

    def _draw_game_replay_status(self):
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


class CLIPlay(CLIMixin):
    def __init__(self, cls_manager):
        super(CLIPlay, self).__init__()
        if not issubclass(cls_manager, UpdateManager):
            raise NotImplementedError
        self.cls_manager = cls_manager
        self.file_name = None
        self.manager = None

    def init(self):
        self.file_name = input('save file name (press ENTER for new game): ')
        if self.file_name:
            self.manager = self.cls_manager.load(self.file_name)
        else:
            settings = self._create_game_settings()
            self.manager = self.cls_manager.create(**settings)

    def clean(self):
        save_file_name = None

        save_progress = input('save progress? (Y, n) ').lower() or 'y'

        if save_progress == 'y':
            if self.file_name:
                save_file_name = self.file_name
            else:
                save_file_name = input('save file name? (press ENTER to skip) ')

        if save_file_name:
            self.manager.save(save_file_name)

    def draw(self):
        self._draw_game_play_status()

    def _draw_game_play_status(self):
        print()
        event_repr = 'Total Events: {}'.format(len(self.manager.wrapper.events))
        print('\n'.join((event_repr,)))

    def update(self):
        raise NotImplementedError

    def status(self):
        raise NotImplementedError

    def _create_game_settings(self):
        raise NotImplementedError
