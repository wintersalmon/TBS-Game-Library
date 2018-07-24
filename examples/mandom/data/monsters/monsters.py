from mandom.data.monsters import MonsterCode


class Monster(object):
    def __init__(self,
                 code: MonsterCode,
                 damage: int = 0):
        self.code = code
        self.damage = damage

    def __str__(self):
        return 'Monster({name})'.format(name=self.code.name)

    def __repr__(self):
        return str(self)


class MonsterGoblin(Monster):
    def __init__(self):
        super(MonsterGoblin, self).__init__(MonsterCode.Goblin, 1)


class MonsterSkeletonWarrior(Monster):
    def __init__(self):
        super(MonsterSkeletonWarrior, self).__init__(MonsterCode.SkeletonWarrior, 2)


class MonsterOrk(Monster):
    def __init__(self):
        super(MonsterOrk, self).__init__(MonsterCode.Ork, 3)


class MonsterVampire(Monster):
    def __init__(self):
        super(MonsterVampire, self).__init__(MonsterCode.Vampire, 4)


class MonsterGolam(Monster):
    def __init__(self):
        super(MonsterGolam, self).__init__(MonsterCode.Golam, 5)


class MonsterReaper(Monster):
    def __init__(self):
        super(MonsterReaper, self).__init__(MonsterCode.Reaper, 6)


class MonsterSatan(Monster):
    def __init__(self):
        super(MonsterSatan, self).__init__(MonsterCode.Satan, 7)


class MonsterDragon(Monster):
    def __init__(self):
        super(MonsterDragon, self).__init__(MonsterCode.Dragon, 9)
