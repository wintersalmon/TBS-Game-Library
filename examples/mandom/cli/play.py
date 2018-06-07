from typing import Iterable

from mandom.data.events import EventFactory, EventCode
from mandom.cli.mandom import MandomCLIDraw
from mandom.data.status import StatusCode
from mandom.managers import MandomUpdateManager
from tbs.cli import CLIPlay
from tbs.error import ExitGameException, ApiError

"""
ALLOWED_EVENTS_FOR_EACH_STATUS
    
    GAME_INIT
        init_round_event (ROUND)
    
    ROUND
        challenge_dungeon (CHALLENGE or GAME_OVER)
        turn_fold (ROUND)
        turn_draw (TURN)

    TURN
        turn_add_monster_to_dungeon (ROUND)
        turn_remove_weapon_from_hero (ROUND)

    CHALLENGE
        init_round_event (ROUND)
    
    GAME_OVER

"""


class GameApp(CLIPlay):
    allowed_events = dict()

    allowed_events[StatusCode.GAME_INIT] = [EventCode.INIT_ROUND]
    allowed_events[StatusCode.ROUND] = [EventCode.CHALLENGE_DUNGEON, EventCode.TURN_FOLD, EventCode.TURN_DRAW]
    allowed_events[StatusCode.TURN] = [EventCode.TURN_ADD_MONSTER_TO_DUNGEON, EventCode.TURN_REMOVE_WEAPON_FROM_HERO]
    allowed_events[StatusCode.CHALLENGE] = [EventCode.INIT_ROUND]
    allowed_events[StatusCode.GAME_OVER] = []

    event_input_description = {
        EventCode.INIT_ROUND: '(I)nit round',
        EventCode.CHALLENGE_DUNGEON: '(C)hallenge Dungeon',
        EventCode.TURN_FOLD: '(F)old',
        EventCode.TURN_DRAW: '(D)raw',
        EventCode.TURN_ADD_MONSTER_TO_DUNGEON: '(A)dd monster to dungeon',
        EventCode.TURN_REMOVE_WEAPON_FROM_HERO: '(R)emove weapon from hero',
    }

    def __init__(self):
        super().__init__(cls_manager=MandomUpdateManager)

    def update(self):
        try:
            event = self._read_user_input_and_create_event()
            self.manager.update(event)
        except ApiError as e:
            print(e)

    def draw(self):
        MandomCLIDraw.draw(self.manager.wrapper.game)

    def status(self):
        return True

    def _create_game_settings(self):
        return {'player_names': ['player_0', 'player_1', 'player_2', 'player_3']}

    def _read_user_input_and_create_event(self):
        """
            INIT_ROUND = auto()
            CHALLENGE_DUNGEON = auto()
            TURN_FOLD = auto()
            TURN_DRAW = auto()
            TURN_ADD_MONSTER_TO_DUNGEON = auto()
            TURN_REMOVE_WEAPON_FROM_HERO = auto()

        """
        event = None
        player = self.manager.wrapper.game.player_turn_tracker.current_player
        status = self.manager.wrapper.game.status
        while True:
            print()
            print('Status: {}'.format(status.name))
            print('Commands')
            for e in self.allowed_events[status]:
                print('    ', self.event_input_description[e])
            values = input(':').lower()
            print()

            if len(values) == 0:
                raise ExitGameException('exit game exception')
            elif values == 'i':
                event = EventFactory.create(EventCode.INIT_ROUND)
            elif values == 'c':
                event = EventFactory.create(EventCode.CHALLENGE_DUNGEON, params={'player': player})
            elif values == 'f':
                event = EventFactory.create(EventCode.TURN_FOLD, params={'player': player})
            elif values == 'd':
                event = EventFactory.create(EventCode.TURN_DRAW, params={'player': player})
            elif values == 'a':
                event = EventFactory.create(EventCode.TURN_ADD_MONSTER_TO_DUNGEON, params={'player': player})
            elif values == 'r':
                weapon = self.manager.wrapper.game.hero.weapons[0].value
                event = EventFactory.create(EventCode.TURN_REMOVE_WEAPON_FROM_HERO,
                                            params={'player': player, 'weapon': weapon})

            if event is not None:
                break
        return event
