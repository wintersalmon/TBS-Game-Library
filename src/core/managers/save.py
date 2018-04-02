import json

from core.managers import LoadManager


class SaveManager(LoadManager):
    def save(self, file_directory, file_name):
        file_path = self.create_file_path(file_directory, file_name)
        # todo : raise error if file already exist
        with open(file_path, 'w', encoding='utf-8') as save_file:
            json.dump(self.wrapper.encode(), save_file)
