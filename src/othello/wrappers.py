from core.manager import GameWrapper


class OthelloCLIWrapper(GameWrapper):
    def __init__(self, manager):
        super().__init__(manager=manager)

    def __bool__(self):
        return bool(self.manager.game)

    def draw(self):
        markers = [' ', '●', '○']

        for row in range(self.manager.game.board.rows):
            for col in range(self.manager.game.board.cols):
                idx = self.manager.game.board.tiles[row][col]
                print('[{}]'.format(markers[idx]), end='')
            print()
        print()
