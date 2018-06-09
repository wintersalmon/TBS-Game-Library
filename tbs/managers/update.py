from .file import FileManager


class UpdateManager(FileManager):
    def update(self, event):
        try:
            event.update(self.wrapper.game)
        except Exception as e:
            raise
        else:
            self.wrapper.events.append(event)
