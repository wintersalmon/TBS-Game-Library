from .file import FileManager


class UpdateManager(FileManager):
    def update(self, event):
        event.update(self.wrapper.game)
        self.wrapper.events.append(event)
