from .save import SaveManager


class UpdateManager(SaveManager):
    def update(self, event):
        try:
            event.update(self.wrapper.game)
        except Exception as e:
            raise e
        else:
            self.wrapper.events.append(event)

    def __str__(self):
        title = 'Game Update Manager'
        event_repr = 'Total Events: {}'.format(len(self.wrapper.events))
        game_repr = super().__str__()
        return '\n'.join((title, event_repr, game_repr))
