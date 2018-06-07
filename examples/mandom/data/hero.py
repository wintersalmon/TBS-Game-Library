from typing import Iterable

from mandom.data.weapons import WeaponCode, WeaponFactory
from tbs.utils import SerializableMixin


class BaseHero(object):
    def __init__(self,
                 default_armor: int,
                 default_weapons: Iterable[WeaponCode]):
        self._default_armor = default_armor
        self._default_weapons = tuple(default_weapons)

    @property
    def default_armor(self):
        return self._default_armor

    @property
    def default_weapons(self):
        return self._default_weapons


class Hero(BaseHero, SerializableMixin):
    def __init__(self, weapons: Iterable[WeaponCode] = None):
        super(Hero, self).__init__(
            default_armor=3,
            default_weapons=WeaponFactory.code_keys())

        if weapons is None:
            self._weapons = {w: True for w in self._default_weapons}
        else:
            self._weapons = {w: False for w in self._default_weapons}
            for w in weapons:
                self._weapons[w] = True

    def encode(self):
        return {
            'weapons': [w.value for w in self.weapons]
        }

    @classmethod
    def decode(cls, **kwargs):
        weapons = [WeaponCode(w) for w in kwargs['weapons']]
        return cls(weapons=weapons)

    @property
    def armor(self):
        return self.default_armor + sum(WeaponFactory.get(w).armor for w in self.weapons)

    @property
    def weapons(self):
        return [weapon for weapon, is_active in self._weapons.items() if is_active]

    def enable_weapon(self, weapon: WeaponCode):
        self._weapons[weapon] = True

    def disable_weapon(self, weapon: WeaponCode):
        self._weapons[weapon] = False

    def restore_to_default_equipment(self):
        for w in self._weapons.keys():
            self._weapons[w] = True
