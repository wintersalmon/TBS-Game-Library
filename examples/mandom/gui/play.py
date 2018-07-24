from kivy.app import App

from mandom.data.events import EventCode, MandomEventFactory
from mandom.data.status import StatusCode
from mandom.gui.mandom import Mandom
from mandom.managers import MandomUpdateManager
from tbs.error import ApiError

allowed_events = dict()

allowed_events[StatusCode.GAME_INIT] = [EventCode.INIT_ROUND]
allowed_events[StatusCode.ROUND] = [EventCode.CHALLENGE_DUNGEON, EventCode.TURN_FOLD, EventCode.TURN_DRAW]
allowed_events[StatusCode.TURN] = [EventCode.TURN_ADD_MONSTER_TO_DUNGEON, EventCode.TURN_REMOVE_WEAPON_FROM_HERO]
allowed_events[StatusCode.CHALLENGE] = [EventCode.INIT_ROUND]
allowed_events[StatusCode.GAME_OVER] = []


class MandomPlay(Mandom):
    def __init__(self, manager, **kwargs):
        super(MandomPlay, self).__init__(manager.wrapper.game, **kwargs)
        self.manager = manager

    def on_touch_down(self, touch):
        if self.manager.wrapper.game.status == StatusCode.GAME_OVER:
            return False

        event = None
        if self.manager.wrapper.game.status in (StatusCode.GAME_INIT, StatusCode.CHALLENGE):
            event = MandomEventFactory.create(EventCode.INIT_ROUND.value)

        else:
            player = self.manager.wrapper.game.player_turn_tracker.current_player

            if self.manager.wrapper.game.status == StatusCode.ROUND:

                if self.ids.dungeon_container.collide_point(*touch.pos):
                    event = MandomEventFactory.create(EventCode.CHALLENGE_DUNGEON.value, player=player)
                elif self.ids.deck_container.collide_point(*touch.pos):
                    event = MandomEventFactory.create(EventCode.TURN_DRAW.value, player=player)
                elif self.ids.player_container.collide_point(*touch.pos):
                    event = MandomEventFactory.create(EventCode.TURN_FOLD.value, player=player)

            elif self.manager.wrapper.game.status == StatusCode.TURN:

                if self.ids.deck_container.collide_point(*touch.pos):
                    event = MandomEventFactory.create(EventCode.TURN_ADD_MONSTER_TO_DUNGEON.value, player=player)
                else:
                    for w_widget in self.ids.weapon_container.children[:]:
                        if w_widget.collide_point(*touch.pos):
                            weapon = w_widget.weapon_code
                            event = MandomEventFactory.create(
                                EventCode.TURN_REMOVE_WEAPON_FROM_HERO.value,
                                player=player,
                                weapon=weapon)

        if event is not None:
            try:
                self.manager.update(event)
            except ApiError as e:
                print(e)
            else:
                return True
        return False


class MandomApp(App):
    def build(self):
        settings = {
            'player_names': ['player_{}'.format(i) for i in range(4)]
        }
        manager = MandomUpdateManager.create(**settings)
        game = MandomPlay(manager=manager)
        return game


GameApp = MandomApp
