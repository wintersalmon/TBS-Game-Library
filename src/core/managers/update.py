from .save import SaveManager


class UpdateManager(SaveManager):
    def update(self, event):
        try:
            event.update(self.wrapper.game)
        except Exception as e:
            raise e
        else:
            self.wrapper.events.append(event)
