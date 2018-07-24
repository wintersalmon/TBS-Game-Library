from mandom.data.weapons.code import WeaponCode
from mandom.data.weapons.weapons import WeaponArmor
from mandom.data.weapons.weapons import WeaponHeroSword
from mandom.data.weapons.weapons import WeaponHolyGrail
from mandom.data.weapons.weapons import WeaponShield
from mandom.data.weapons.weapons import WeaponSpear
from mandom.data.weapons.weapons import WeaponTorch


class WeaponFactory(object):
    WEAPONS = {
        WeaponCode.Torch: WeaponTorch(),
        WeaponCode.HolyGrail: WeaponHolyGrail(),
        WeaponCode.Spear: WeaponSpear(),
        WeaponCode.Armor: WeaponArmor(),
        WeaponCode.Shield: WeaponShield(),
        WeaponCode.HeroSword: WeaponHeroSword(),
    }

    WEAPONS_BY_CODE = {
        WeaponCode.Torch: WEAPONS[WeaponCode.Torch],
        WeaponCode.HolyGrail: WEAPONS[WeaponCode.HolyGrail],
        WeaponCode.Spear: WEAPONS[WeaponCode.Spear],
        WeaponCode.Armor: WEAPONS[WeaponCode.Armor],
        WeaponCode.Shield: WEAPONS[WeaponCode.Shield],
        WeaponCode.HeroSword: WEAPONS[WeaponCode.HeroSword],
    }

    WEAPONS_BY_NUMBER = {
        int(WeaponCode.Torch.value): WEAPONS[WeaponCode.Torch],
        int(WeaponCode.HolyGrail.value): WEAPONS[WeaponCode.HolyGrail],
        int(WeaponCode.Spear.value): WEAPONS[WeaponCode.Spear],
        int(WeaponCode.Armor.value): WEAPONS[WeaponCode.Armor],
        int(WeaponCode.Shield.value): WEAPONS[WeaponCode.Shield],
        int(WeaponCode.HeroSword.value): WEAPONS[WeaponCode.HeroSword],
    }

    WEAPONS_BY_STRING = {
        WeaponCode.Torch.name.lower(): WEAPONS[WeaponCode.Torch],
        WeaponCode.HolyGrail.name.lower(): WEAPONS[WeaponCode.HolyGrail],
        WeaponCode.Spear.name.lower(): WEAPONS[WeaponCode.Spear],
        WeaponCode.Armor.name.lower(): WEAPONS[WeaponCode.Armor],
        WeaponCode.Shield.name.lower(): WEAPONS[WeaponCode.Shield],
        WeaponCode.HeroSword.name.lower(): WEAPONS[WeaponCode.HeroSword],
    }

    @classmethod
    def code_keys(cls):
        return cls.WEAPONS_BY_CODE.keys()

    @classmethod
    def number_keys(cls):
        return cls.WEAPONS_BY_NUMBER.keys()

    @classmethod
    def string_keys(cls):
        return cls.WEAPONS_BY_STRING.keys()

    @classmethod
    def get(cls, weapon):
        if isinstance(weapon, WeaponCode):
            return cls.WEAPONS_BY_CODE[weapon]
        elif isinstance(weapon, int):
            return cls.WEAPONS_BY_NUMBER[weapon]
        elif isinstance(weapon, str):
            return cls.WEAPONS_BY_STRING[weapon.lower()]
        raise NotImplementedError('invalid type (must be WeaponCode | int | str): {}'.format(type(weapon)))


if __name__ == '__main__':
    a = WeaponFactory.get(WeaponCode.Torch)
    b = WeaponFactory.get('torch')
    c = WeaponFactory.get(1)
    print(a, b, c, a == b == c)
    print(id(a), id(b), id(c))
