class OthelloCLIDrawMixin(object):
    VIEW_MARKERS = [' ', '○', '●', '-']

    @classmethod
    def draw_status(cls, game):
        status = 'running' if bool(game.status) else 'stopped'
        player = cls.VIEW_MARKERS[game.status.player]
        black_count, white_count = game.board.count

        print('Game   {}'.format(status))
        print('Turn   {}'.format(player))
        print('Score  {}{} : {}{}'.format(cls.VIEW_MARKERS[1], black_count, cls.VIEW_MARKERS[2], white_count))

    @classmethod
    def draw_board(cls, game, *, detailed=False):
        player = game.status.player

        rows = list()
        rows.append('   ' + ''.join(' {} '.format(c) for c in range(game.board.cols)))  # add colon numbers
        for r in range(game.board.rows):
            cols = list()
            cols.append(' {} '.format(r))  # add line number
            for c in range(game.board.cols):
                tile = cls.create_tile_marker(game, r, c, player, detailed=detailed)
                cols.append(tile)
            rows.append(''.join(cols))

        print('\n'.join(rows))

    @classmethod
    def create_tile_marker(cls, game, r, c, player, *, detailed=False):
        if game.board.is_set(r, c):
            tile = ' {} '.format(cls.VIEW_MARKERS[game.board.get(r, c)])
        else:
            positions = game.board.find_flip_positions(r, c, player)

            if positions:
                if detailed:
                    tile = '{:2} '.format(positions)
                else:
                    tile = '[ ]'
            else:
                tile = '   '

        return tile
