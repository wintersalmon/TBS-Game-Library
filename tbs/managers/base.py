import json
import os

from tbs.wrapper import Wrapper


class Manager(object):
    cls_wrapper = Wrapper
    base_save_dir = None

    def __init__(self, wrapper=None):
        self.wrapper = wrapper

    @classmethod
    def create_file_path(cls, file_directory, file_name):
        return os.path.join(file_directory, '{}.json'.format(file_name))

    @classmethod
    def load(cls, file_name, *, other_directory=None):
        if other_directory:
            file_directory = other_directory
        else:
            file_directory = cls.base_save_dir
        file_path = cls.create_file_path(file_directory, file_name)

        with open(file_path, 'r', encoding='utf-8') as load_file:
            data = json.load(load_file)
            wrapper = cls.cls_wrapper.decode(**data)
            return cls(wrapper=wrapper)

    @classmethod
    def create(cls, **settings):
        wrapper = cls.cls_wrapper.create(**settings)
        return cls(wrapper=wrapper)
