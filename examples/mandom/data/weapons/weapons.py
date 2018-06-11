from typing import Iterable

from mandom.data.monsters import MonsterCode
from mandom.data.weapons import WeaponCode


class Weapon(object):
    def __init__(self,
                 code: WeaponCode,
                 armor: int,
                 slayer_monsters: Iterable[MonsterCode] = None):
        self.code = code
        self.armor = armor
        self.slayer_monsters = tuple() if slayer_monsters is None else slayer_monsters

    def __str__(self):
        return 'Weapon({name})'.format(name=self.code.name)

    def __repr__(self):
        return str(self)


class HeroWeapon(Weapon):
    def __init__(self, code, armor):
        super(HeroWeapon, self).__init__(code=code, armor=armor)

    def change_slayer_monster(self, slayer_monster: MonsterCode):
        self.slayer_monsters = (slayer_monster,)


class WeaponTorch(Weapon):
    def __init__(self):
        super(WeaponTorch, self).__init__(WeaponCode.Torch, 0,
                                          (MonsterCode.Goblin, MonsterCode.SkeletonWarrior, MonsterCode.Ork))


class WeaponHolyGrail(Weapon):
    def __init__(self):
        super(WeaponHolyGrail, self).__init__(WeaponCode.HolyGrail, 0,
                                              (MonsterCode.SkeletonWarrior, MonsterCode.Vampire, MonsterCode.Reaper))


class WeaponSpear(Weapon):
    def __init__(self):
        super(WeaponSpear, self).__init__(WeaponCode.Spear, 0,
                                          (MonsterCode.Dragon,))


class WeaponArmor(Weapon):
    def __init__(self):
        super(WeaponArmor, self).__init__(WeaponCode.Armor, 5)


class WeaponShield(Weapon):
    def __init__(self):
        super(WeaponShield, self).__init__(WeaponCode.Shield, 3)


class WeaponHeroSword(HeroWeapon):
    def __init__(self):
        super(WeaponHeroSword, self).__init__(WeaponCode.HeroSword, 0)
