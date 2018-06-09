from mandom.data.weapons.code import WeaponCode
from mandom.data.weapons.weapons import WeaponArmor
from mandom.data.weapons.weapons import WeaponHeroSword
from mandom.data.weapons.weapons import WeaponHolyGrail
from mandom.data.weapons.weapons import WeaponShield
from mandom.data.weapons.weapons import WeaponSpear
from mandom.data.weapons.weapons import WeaponTorch


class WeaponFactory(object):
    WEAPONS = {
        WeaponCode.TORCH: WeaponTorch(),
        WeaponCode.HOLY_GRAIL: WeaponHolyGrail(),
        WeaponCode.SPEAR: WeaponSpear(),
        WeaponCode.ARMOR: WeaponArmor(),
        WeaponCode.SHIELD: WeaponShield(),
        WeaponCode.HERO_SWORD: WeaponHeroSword(),
    }

    WEAPONS_BY_CODE = {
        WeaponCode.TORCH: WEAPONS[WeaponCode.TORCH],
        WeaponCode.HOLY_GRAIL: WEAPONS[WeaponCode.HOLY_GRAIL],
        WeaponCode.SPEAR: WEAPONS[WeaponCode.SPEAR],
        WeaponCode.ARMOR: WEAPONS[WeaponCode.ARMOR],
        WeaponCode.SHIELD: WEAPONS[WeaponCode.SHIELD],
        WeaponCode.HERO_SWORD: WEAPONS[WeaponCode.HERO_SWORD],
    }

    WEAPONS_BY_NUMBER = {
        int(WeaponCode.TORCH.value): WEAPONS[WeaponCode.TORCH],
        int(WeaponCode.HOLY_GRAIL.value): WEAPONS[WeaponCode.HOLY_GRAIL],
        int(WeaponCode.SPEAR.value): WEAPONS[WeaponCode.SPEAR],
        int(WeaponCode.ARMOR.value): WEAPONS[WeaponCode.ARMOR],
        int(WeaponCode.SHIELD.value): WEAPONS[WeaponCode.SHIELD],
        int(WeaponCode.HERO_SWORD.value): WEAPONS[WeaponCode.HERO_SWORD],
    }

    WEAPONS_BY_STRING = {
        WeaponCode.TORCH.name.lower(): WEAPONS[WeaponCode.TORCH],
        WeaponCode.HOLY_GRAIL.name.lower(): WEAPONS[WeaponCode.HOLY_GRAIL],
        WeaponCode.SPEAR.name.lower(): WEAPONS[WeaponCode.SPEAR],
        WeaponCode.ARMOR.name.lower(): WEAPONS[WeaponCode.ARMOR],
        WeaponCode.SHIELD.name.lower(): WEAPONS[WeaponCode.SHIELD],
        WeaponCode.HERO_SWORD.name.lower(): WEAPONS[WeaponCode.HERO_SWORD],
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
    a = WeaponFactory.get(WeaponCode.TORCH)
    b = WeaponFactory.get('torch')
    c = WeaponFactory.get(1)
    print(a, b, c, a == b == c)
    print(id(a), id(b), id(c))
