import random
from typing import Iterable

from mandom.data.monsters import MonsterCode, MonsterStack
from tbs.utils import SerializableMixin


class Deck(SerializableMixin):

    def __init__(self, cards: Iterable[MonsterCode] = None):
        self._default_cards = [
            MonsterCode.Goblin,
            MonsterCode.Goblin,
            MonsterCode.SkeletonWarrior,
            MonsterCode.SkeletonWarrior,
            MonsterCode.Ork,
            MonsterCode.Ork,
            MonsterCode.Vampire,
            MonsterCode.Vampire,
            MonsterCode.Golam,
            MonsterCode.Golam,
            MonsterCode.Reaper,
            MonsterCode.Satan,
            MonsterCode.Dragon,
        ]

        if cards is None:
            self._cards = MonsterStack()
        else:
            self._cards = MonsterStack(cards)

    def __len__(self):
        return len(self._cards)

    def __getitem__(self, key):
        return self._cards[key]

    def __iter__(self):
        return iter(self._cards)

    def view_default_card_set(self):
        return self._default_cards[:]

    def draw(self):
        return self._cards.pop()

    def view_top_card(self):
        return self._cards.peek()

    def return_to_top(self, monster: MonsterCode):
        self._cards.push(monster)

    def encode(self):
        return {
            'cards': [monster.value for monster in self._cards]
        }

    @classmethod
    def decode(cls, **kwargs):
        cards = [MonsterCode(m) for m in kwargs['cards']]
        return cls(cards=cards)

    def restore_and_shuffle(self, seed: int):
        cards = self._default_cards[:]
        random.Random(seed).shuffle(cards)
        self._cards = MonsterStack(cards)
