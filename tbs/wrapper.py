import json
import os

from tbs.utils import SerializableMixin


class Wrapper(SerializableMixin):
    def __init__(self, settings, game, events):
        self.settings = settings
        self.game = game
        self.events = events

    def draw(self):
        pass

    def encode(self):
        raise NotImplementedError

    @classmethod
    def decode(cls, **kwargs):
        raise NotImplementedError

    @classmethod
    def create(cls, **kwargs):
        raise NotImplementedError


class LoadFileMixin(object):
    @staticmethod
    def _create_file_path(file_directory, file_name):
        return os.path.join(file_directory, '{}.json'.format(file_name))

    def _load_data(self, file_directory, file_name):
        file_path = self._create_file_path(file_directory, file_name)
        with open(file_path, 'r', encoding='utf-8') as load_file:
            return json.load(load_file)

    @classmethod
    def load(cls, file_directory, file_name):
        raise NotImplementedError

