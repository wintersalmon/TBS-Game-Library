import json
import os

from .base import Manager


class LoadManager(Manager):
    def __init__(self, wrapper):
        super().__init__(wrapper=wrapper)

    @classmethod
    def create_file_path(cls, file_directory, file_name):
        return os.path.join(file_directory, '{}.json'.format(file_name))

    @classmethod
    def load(cls, cls_wrapper, file_directory, file_name):
        file_path = cls.create_file_path(file_directory, file_name)
        # todo : raise error if file does not exist
        with open(file_path, 'r', encoding='utf-8') as load_file:
            data = json.load(load_file)
            wrapper = cls_wrapper.decode(**data)
            return cls(wrapper=wrapper)