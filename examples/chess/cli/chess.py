class ChessCLIDrawMixin(object):
    COL_NUMBERS = ' '.join([' ', '0', '1', '2', '3', '4', '5', '6', '7'])

    @classmethod
    def draw_board(cls, game):
        lines = list()

        lines.append(cls.COL_NUMBERS)
        for r, rows in enumerate(game.board.tiles):
            line = list()
            line.append(str(r))  # add line number
            for c, col in enumerate(rows):
                if game.board.is_set(r, c):
                    marker = col.nickname
                else:
                    marker = ' '
                line.append(marker)
            lines.append(' '.join(line))

        print('\n'.join(lines))

    @classmethod
    def draw_players(cls, game):
        print('players: {}'.format([player.name for player in game.players]))

    @classmethod
    def draw(cls, game):
        cls.draw_players(game)
        cls.draw_board(game)
