from typing import Iterable

from mandom.data.monsters import MonsterCode
from tbs.container import Stack
from tbs.utils import SerializableMixin


class MonsterStack(Stack, SerializableMixin):

    def __init__(self, items: Iterable[MonsterCode] = None):
        super(MonsterStack, self).__init__(items=items)

    def encode(self):
        return {
            'items': [m.value for m in iter(self)]
        }

    @classmethod
    def decode(cls, **kwargs):
        items = [MonsterCode(i) for i in kwargs['items']]
        return MonsterStack(items=items)
