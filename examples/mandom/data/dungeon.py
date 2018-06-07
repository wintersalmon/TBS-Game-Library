from typing import Iterable

from mandom.data.monsters import MonsterCode, MonsterFactory, MonsterStack
from mandom.data.weapons import WeaponFactory


class Dungeon(MonsterStack):
    def __init__(self, items: Iterable[MonsterCode] = None):
        super(Dungeon, self).__init__(items=items)

    def challenge(self, hero):
        armor = hero.armor
        weapons = [WeaponFactory.get(w) for w in hero.weapons]
        monsters = [MonsterFactory.get(m) for m in iter(self)]

        slayer_monsters = set()
        for w in weapons:
            slayer_monsters.update(w.slayer_monsters)
        for monster in monsters:
            if monster.code not in slayer_monsters:
                armor -= monster.damage
        return armor

    @classmethod
    def decode(cls, **kwargs):
        items = [MonsterCode(i) for i in kwargs['items']]
        return Dungeon(items=items)
