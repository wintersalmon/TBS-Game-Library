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
        super(WeaponTorch, self).__init__(WeaponCode.TORCH, 0,
                                          (MonsterCode.GOBLIN, MonsterCode.SKELETON_WARRIOR, MonsterCode.ORK))


class WeaponHolyGrail(Weapon):
    def __init__(self):
        super(WeaponHolyGrail, self).__init__(WeaponCode.HOLY_GRAIL, 0,
                                              (MonsterCode.SKELETON_WARRIOR, MonsterCode.VAMPIRE, MonsterCode.REAPER))


class WeaponSpear(Weapon):
    def __init__(self):
        super(WeaponSpear, self).__init__(WeaponCode.SPEAR, 0,
                                          (MonsterCode.DRAGON,))


class WeaponArmor(Weapon):
    def __init__(self):
        super(WeaponArmor, self).__init__(WeaponCode.ARMOR, 5)


class WeaponShield(Weapon):
    def __init__(self):
        super(WeaponShield, self).__init__(WeaponCode.SHIELD, 3)


class WeaponHeroSword(HeroWeapon):
    def __init__(self):
        super(WeaponHeroSword, self).__init__(WeaponCode.HERO_SWORD, 0)
