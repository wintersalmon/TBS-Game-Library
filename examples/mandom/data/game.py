from typing import List

from mandom.data.deck import Deck
from mandom.data.dungeon import Dungeon
from mandom.data.hero import Hero
from mandom.data.monsters import MonsterStack
from mandom.data.player import PlayerTurnTracker
from mandom.data.status import StatusCode
from mandom.data.weapons import WeaponStack
from tbs.player import Player
from tbs.utils import SerializableMixin


class MandomGame(SerializableMixin):
    def __init__(self,
                 players: List[Player],
                 hero: Hero = None,
                 deck: Deck = None,
                 dungeon: Dungeon = None,
                 removed_monsters: MonsterStack = None,
                 removed_weapons: WeaponStack = None,
                 player_turn_tracker: PlayerTurnTracker = None,
                 status: StatusCode = None):
        self.players = players
        self.hero = Hero() if hero is None else hero
        self.deck = Deck() if deck is None else deck
        self.dungeon = Dungeon() if dungeon is None else dungeon
        self.removed_monsters = MonsterStack() if removed_monsters is None else removed_monsters
        self.removed_weapons = WeaponStack() if removed_weapons is None else removed_weapons
        self.player_turn_tracker = PlayerTurnTracker(
            list(range(len(players)))) if player_turn_tracker is None else player_turn_tracker
        self.status = StatusCode.GAME_INIT if status is None else status

    def encode(self):
        return {
            'players': [p.encode() for p in self.players],
            'hero': self.hero.encode(),
            'deck': self.deck.encode(),
            'dungeon': self.dungeon.encode(),
            'removed_monsters': self.removed_monsters.encode(),
            'removed_weapons': self.removed_weapons.encode(),
            'player_turn_tracker': self.player_turn_tracker.encode(),
            'status': self.status.value,
        }

    @classmethod
    def decode(cls, **kwargs):
        players = [Player.decode(**p) for p in kwargs['players']]
        hero = Hero.decode(**kwargs['hero'])
        deck = Deck.decode(**kwargs['deck'])
        dungeon = Dungeon.decode(**kwargs['dungeon'])
        removed_monsters = MonsterStack.decode(**kwargs['removed_monsters'])
        removed_weapons = WeaponStack.decode(**kwargs['removed_weapons'])
        player_turn_tracker = PlayerTurnTracker.decode(**kwargs['player_turn_tracker'])
        status = StatusCode(int(kwargs['status']))if 'status' in kwargs else None
        return cls(
            players=players,
            hero=hero,
            deck=deck,
            dungeon=dungeon,
            removed_monsters=removed_monsters,
            removed_weapons=removed_weapons,
            player_turn_tracker=player_turn_tracker,
            status=status)
