import json

from .base import Manager


class FileManager(Manager):
    def __init__(self, wrapper=None):
        super(FileManager, self).__init__(wrapper=wrapper)

    def save(self, file_name, other_directory=None):
        if other_directory:
            file_directory = other_directory
        else:
            file_directory = self.base_save_dir
        file_path = self.create_file_path(file_directory, file_name)
        with open(file_path, 'w', encoding='utf-8') as save_file:
            json.dump(self.wrapper.encode(), save_file)
