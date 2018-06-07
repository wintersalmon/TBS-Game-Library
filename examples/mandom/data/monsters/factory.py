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
        MonsterCode.GOBLIN: MonsterGoblin(),
        MonsterCode.SKELETON_WARRIOR: MonsterSkeletonWarrior(),
        MonsterCode.ORK: MonsterOrk(),
        MonsterCode.VAMPIRE: MonsterVampire(),
        MonsterCode.GOLAM: MonsterGolam(),
        MonsterCode.REAPER: MonsterReaper(),
        MonsterCode.SATAN: MonsterSatan(),
        MonsterCode.DRAGON: MonsterDragon(),
    }

    MONSTERS_BY_NUMBER = {
        int(MonsterCode.GOBLIN.value): MONSTERS[MonsterCode.GOBLIN],
        int(MonsterCode.SKELETON_WARRIOR.value): MONSTERS[MonsterCode.SKELETON_WARRIOR],
        int(MonsterCode.ORK.value): MONSTERS[MonsterCode.ORK],
        int(MonsterCode.VAMPIRE.value): MONSTERS[MonsterCode.VAMPIRE],
        int(MonsterCode.GOLAM.value): MONSTERS[MonsterCode.GOLAM],
        int(MonsterCode.REAPER.value): MONSTERS[MonsterCode.REAPER],
        int(MonsterCode.SATAN.value): MONSTERS[MonsterCode.SATAN],
        int(MonsterCode.DRAGON.value): MONSTERS[MonsterCode.DRAGON],
    }

    MONSTERS_BY_STRING = {
        MonsterCode.GOBLIN.name.lower(): MONSTERS[MonsterCode.GOBLIN],
        MonsterCode.SKELETON_WARRIOR.name.lower(): MONSTERS[MonsterCode.SKELETON_WARRIOR],
        MonsterCode.ORK.name.lower(): MONSTERS[MonsterCode.ORK],
        MonsterCode.VAMPIRE.name.lower(): MONSTERS[MonsterCode.VAMPIRE],
        MonsterCode.GOLAM.name.lower(): MONSTERS[MonsterCode.GOLAM],
        MonsterCode.REAPER.name.lower(): MONSTERS[MonsterCode.REAPER],
        MonsterCode.SATAN.name.lower(): MONSTERS[MonsterCode.SATAN],
        MonsterCode.DRAGON.name.lower(): MONSTERS[MonsterCode.DRAGON],
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
    a = MonsterFactory.get(MonsterCode.GOBLIN)
    b = MonsterFactory.get('goblin')
    c = MonsterFactory.get(1)
    print(a, b, c, a == b == c)
    print(id(a), id(b), id(c))
