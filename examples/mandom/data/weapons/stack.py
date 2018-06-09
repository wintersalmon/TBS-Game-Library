from typing import Iterable

from mandom.data.weapons import WeaponCode
from tbs.container import Stack
from tbs.utils import SerializableMixin


class WeaponStack(Stack, SerializableMixin):

    def __init__(self, items: Iterable[WeaponCode] = None):
        super(WeaponStack, self).__init__(items=items)

    def encode(self):
        return {
            'items': [m.value for m in iter(self)]
        }

    @classmethod
    def decode(cls, **kwargs):
        items = [WeaponCode(i) for i in kwargs['items']]
        return WeaponStack(items=items)
