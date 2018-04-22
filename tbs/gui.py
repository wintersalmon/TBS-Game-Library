from kivy.clock import Clock
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput


class GUIReplay(GridLayout):
    def __init__(self, cls_game_layout, manager, **kwargs):
        super(GUIReplay, self).__init__(**kwargs)
        self.manager = manager
        self.auto_event = False

        self.cols = 1

        self.game_layout = cls_game_layout(game=self.manager.wrapper.game)
        self.add_widget(self.game_layout)

        # control area
        self.control_area = GridLayout(cols=3)
        self.control_area.size_hint_y = None
        self.control_area.height = 200

        self.btn_backward = Button(text='<|')
        self.set_position_input_text = TextInput(hint_text='set (0 <= position <= {}'.format(self.manager.get_max_position()), multiline=False, input_filter="int")
        self.btn_forward = Button(text='|>')

        self.btn_set_begin = Button(text='<<<')
        self.btn_auto_toggle = Button(text='AUTO')
        self.btn_set_end = Button(text='>>>')

        def on_enter(instance):
            pos = int(instance.text)
            if self.manager.set_position(pos):
                instance.text = ''
            else:
                print(pos)

        self.set_position_input_text.bind(on_text_validate=on_enter)

        self.control_area.add_widget(self.btn_backward)
        self.control_area.add_widget(self.set_position_input_text)
        self.control_area.add_widget(self.btn_forward)

        self.control_area.add_widget(self.btn_set_begin)
        self.control_area.add_widget(self.btn_auto_toggle)
        self.control_area.add_widget(self.btn_set_end)

        self.add_widget(self.control_area)

    def toggle_forward(self, dt):
        if self.auto_event and self.manager.forward():
            Clock.schedule_once(self.toggle_forward, .5)
            self.btn_auto_toggle.text = 'STOP'
            return True
        else:
            self.btn_auto_toggle.text = 'AUTO'
            return False

    def on_touch_down(self, touch):
        if self.btn_forward.collide_point(*touch.pos):
            self.manager.forward()
            return True
        elif self.btn_backward.collide_point(*touch.pos):
            self.manager.backward()
            return True
        elif self.btn_set_begin.collide_point(*touch.pos):
            self.manager.set_position(0)
            return True
        elif self.btn_set_end.collide_point(*touch.pos):
            self.manager.set_position(self.manager.get_max_position())
            return True
        elif self.btn_auto_toggle.collide_point(*touch.pos):
            if self.auto_event:
                self.auto_event = False
            else:
                Clock.schedule_once(self.toggle_forward, .1)
                self.auto_event = True
            return True
        else:
            return super(GUIReplay, self).on_touch_down(touch)
