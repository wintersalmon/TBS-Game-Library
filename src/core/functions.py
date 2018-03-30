import json
import os


def create_file_path(file_directory, file_name):
    return os.path.join(file_directory, '{}.json'.format(file_name))


def load_game(file_directory, file_name):
    file_path = create_file_path(file_directory, file_name)
    # todo : raise error if file does not exist
    with open(file_path, 'r', encoding='utf-8') as load_file:
        return json.load(load_file)


def save_game(file_directory, file_name, data):
    file_path = create_file_path(file_directory, file_name)
    # todo : raise error if file already exist
    with open(file_path, 'w', encoding='utf-8') as save_file:
        json.dump(data.encode(), save_file)
