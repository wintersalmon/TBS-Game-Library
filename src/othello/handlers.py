from core.handlers import ManagerFunctionHandler


class OthelloDrawHandler(ManagerFunctionHandler):
    def __init__(self, manager):
        super().__init__(manager)

    def function(self):
        markers = [' ', '●', '○']
        for row in range(self.manager.game.board.rows):
            for col in range(self.manager.game.board.cols):
                idx = self.manager.game.board.tiles[row][col]
                print('[{}]'.format(markers[idx]), end='')
            print()
        print()


class OthelloUpdateHandler(ManagerFunctionHandler):
    def __init__(self, manager):
        super().__init__(manager)

    def function(self, event):
        try:
            event.update(self.manager.game)
        except Exception as e:
            raise e
        else:
            self.manager.events.append(event)
