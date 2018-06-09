import json
import os


class CallableMixin(object):
    def __call__(self, *args, **kwargs):
        raise NotImplementedError


class SerializableMixin(object):
    def encode(self):
        raise NotImplementedError

    @classmethod
    def decode(cls, **kwargs):
        raise NotImplementedError


class ImmutableMixin(object):
    __slots__ = ()


def load_json(file_dir, file_name):
    load_file_path = os.path.join(file_dir, file_name)
    with open(load_file_path, 'r', encoding='utf-8') as infile:
        return json.load(infile)
