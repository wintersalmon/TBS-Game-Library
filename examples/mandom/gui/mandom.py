from kivy.app import App
from kivy.clock import Clock
from kivy.properties import ObjectProperty, BooleanProperty, StringProperty, NumericProperty
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label

from mandom.data.status import StatusCode
from mandom.wrapper import MandomWrapper

DEBUG_MODE = False


class PlayerWidget(GridLayout):
    player_name = StringProperty('NONE')
    player_life_point = NumericProperty(-1)
    player_victory_point = NumericProperty(-1)
    is_active = BooleanProperty(False)

    def __init__(self, player_name, **kwargs):
        super(PlayerWidget, self).__init__(**kwargs)
        self.player_name = player_name


class WeaponWidget(Label):
    weapon_name = StringProperty('NONE')
    is_active = BooleanProperty(False)

    def __init__(self, weapon_code, **kwargs):
        super(WeaponWidget, self).__init__(**kwargs)
        self.weapon_code = weapon_code
        self.weapon_name = weapon_code.name.title()


class MonsterWidget(Label):
    monster_name = StringProperty('NONE')
    is_visible = BooleanProperty(False)
    is_active = BooleanProperty(False)

    def __init__(self, position_in_container, **kwargs):
        super(MonsterWidget, self).__init__(**kwargs)
        self.position_in_container = position_in_container


class Mandom(GridLayout):
    game = ObjectProperty(None)

    def __init__(self, game, **kwargs):
        super(Mandom, self).__init__(**kwargs)
        self.cols = 1
        self.game = game
        self.debug_mode = DEBUG_MODE
        # self.refresh_widgets = list()

        self.player_widgets = list()
        for p in self.game.players:
            p_widget = PlayerWidget(p.name)
            self.player_widgets.append(p_widget)
            self.ids.player_container.add_widget(p_widget)

        self.ids.hero_container.text = str(self.game.hero.default_armor)

        self.weapons_widgets = list()
        for weapon in self.game.hero.default_weapons:
            w_widget = WeaponWidget(weapon)
            self.weapons_widgets.append(w_widget)
            self.ids.weapon_container.add_widget(w_widget)

        self.monsters_in_deck = list()
        self.monsters_in_dungeon = list()
        for i, m in enumerate(self.game.deck.view_default_card_set()):
            # deck
            m_widget = MonsterWidget(i)
            m_widget.is_visible = self.debug_mode
            self.monsters_in_deck.append(m_widget)
            self.ids.deck_container.add_widget(m_widget)

            # dungeon
            m_widget = MonsterWidget(i)
            m_widget.is_visible = self.debug_mode
            self.monsters_in_dungeon.append(m_widget)
            self.ids.dungeon_container.add_widget(m_widget)

        Clock.schedule_interval(self.draw, 1.0 / 10.0)

    def draw(self, dt):
        status = self.game.status.name if self.game and self.game.status else 'error'
        self.ids.game_status_container.text = 'STATUS: {}'.format(status)

        for player_position, p_widget in enumerate(self.player_widgets):
            player = self.game.players[player_position]
            p_widget.player_name = player.name
            p_widget.player_life_point = player.life_point
            p_widget.player_victory_point = player.victory_point
            p_widget.is_active = player_position in self.game.player_turn_tracker.players

        for w_widget in self.weapons_widgets:
            weapon = w_widget.weapon_code
            w_widget.is_active = weapon in self.game.hero.weapons

        for m_widget in self.monsters_in_deck:
            position = m_widget.position_in_container
            if position < len(self.game.deck):
                m_widget.is_active = True
                m_widget.is_visible = position == len(self.game.deck) - 1 and self.game.status == StatusCode.TURN
                m_widget.monster_name = self.game.deck[position].name.title()
            else:
                m_widget.is_active = False

        for m_widget in self.monsters_in_dungeon:
            position = m_widget.position_in_container
            if position < len(self.game.dungeon):
                m_widget.is_active = True
                m_widget.is_visible = self.game.status == StatusCode.CHALLENGE
                m_widget.monster_name = self.game.dungeon[position].name.title()
            else:
                m_widget.is_active = False

        if self.game.status == StatusCode.TURN:
            self.ids.selected_card.text = self.game.deck.view_top_card().name.title()
        else:
            self.ids.selected_card.text = ''


class MandomApp(App):

    def build(self):
        settings = {
            'player_names': ['player_{}'.format(i) for i in range(4)]
        }
        wrapper = MandomWrapper.create(**settings)
        game = Mandom(game=wrapper.game)
        return game


if __name__ == '__main__':
    MandomApp().run()
