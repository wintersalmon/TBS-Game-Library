from mandom.data.monsters import MonsterCode
from mandom.data.monsters.monsters import MonsterDragon
from mandom.data.monsters.monsters import MonsterGoblin
from mandom.data.monsters.monsters import MonsterGolam
from mandom.data.monsters.monsters import MonsterOrk
from mandom.data.monsters.monsters import MonsterReaper
from mandom.data.monsters.monsters import MonsterSatan
from mandom.data.monsters.monsters import MonsterSkeletonWarrior
from mandom.data.monsters.monsters import MonsterVampire


class MonsterFactory(object):
    MONSTERS = {
        MonsterCode.Goblin: MonsterGoblin(),
        MonsterCode.SkeletonWarrior: MonsterSkeletonWarrior(),
        MonsterCode.Ork: MonsterOrk(),
        MonsterCode.Vampire: MonsterVampire(),
        MonsterCode.Golam: MonsterGolam(),
        MonsterCode.Reaper: MonsterReaper(),
        MonsterCode.Satan: MonsterSatan(),
        MonsterCode.Dragon: MonsterDragon(),
    }

    MONSTERS_BY_NUMBER = {
        int(MonsterCode.Goblin.value): MONSTERS[MonsterCode.Goblin],
        int(MonsterCode.SkeletonWarrior.value): MONSTERS[MonsterCode.SkeletonWarrior],
        int(MonsterCode.Ork.value): MONSTERS[MonsterCode.Ork],
        int(MonsterCode.Vampire.value): MONSTERS[MonsterCode.Vampire],
        int(MonsterCode.Golam.value): MONSTERS[MonsterCode.Golam],
        int(MonsterCode.Reaper.value): MONSTERS[MonsterCode.Reaper],
        int(MonsterCode.Satan.value): MONSTERS[MonsterCode.Satan],
        int(MonsterCode.Dragon.value): MONSTERS[MonsterCode.Dragon],
    }

    MONSTERS_BY_STRING = {
        MonsterCode.Goblin.name.lower(): MONSTERS[MonsterCode.Goblin],
        MonsterCode.SkeletonWarrior.name.lower(): MONSTERS[MonsterCode.SkeletonWarrior],
        MonsterCode.Ork.name.lower(): MONSTERS[MonsterCode.Ork],
        MonsterCode.Vampire.name.lower(): MONSTERS[MonsterCode.Vampire],
        MonsterCode.Golam.name.lower(): MONSTERS[MonsterCode.Golam],
        MonsterCode.Reaper.name.lower(): MONSTERS[MonsterCode.Reaper],
        MonsterCode.Satan.name.lower(): MONSTERS[MonsterCode.Satan],
        MonsterCode.Dragon.name.lower(): MONSTERS[MonsterCode.Dragon],
    }

    @classmethod
    def code_keys(cls):
        return cls.MONSTERS.keys()

    @classmethod
    def number_keys(cls):
        return cls.MONSTERS_BY_NUMBER.keys()

    @classmethod
    def string_keys(cls):
        return cls.MONSTERS_BY_STRING.keys()

    @classmethod
    def get(cls, monster):
        if isinstance(monster, MonsterCode):
            return cls.MONSTERS[monster]
        elif isinstance(monster, int):
            return cls.MONSTERS_BY_NUMBER[monster]
        elif isinstance(monster, str):
            return cls.MONSTERS_BY_STRING[monster.lower()]
        raise NotImplementedError('invalid type (must be MonsterCode | int | str): {}'.format(type(monster)))


if __name__ == '__main__':
    a = MonsterFactory.get(MonsterCode.Goblin)
    b = MonsterFactory.get('goblin')
    c = MonsterFactory.get(1)
    print(a, b, c, a == b == c)
    print(id(a), id(b), id(c))
