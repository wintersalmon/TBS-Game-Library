class MandomCLIDraw(object):
    @classmethod
    def draw_player(cls, player):
        player_fmt = 'Player(name={name} vp={vp} lp={lp})'

        return player_fmt.format(
            name=player.name,
            vp=player.victory_point,
            lp=player.life_point,
        )

    @classmethod
    def draw(cls, game):
        for p, player in enumerate(game.players):
            player_fmt = cls.draw_player(player)

            marker = 'X'
            if len(game.player_turn_tracker) > 0:
                active_player = p in game.player_turn_tracker.players
                current_turn_player = p == game.player_turn_tracker.current_player

                if active_player:
                    if current_turn_player:
                        marker = '*'
                    else:
                        marker = ' '

            print('[{}] {}'.format(marker, player_fmt))

        print('weapons_enabled: {}'.format([w.name for w in game.hero.weapons]))
        print('monsters_deck: {}'.format([m.name for m in game.deck]))
        print('monsters_dungeon: {}'.format([m.name for m in game.dungeon]))
        print('monsters_removed: {}'.format([m.name for m in game.removed_monsters]))
