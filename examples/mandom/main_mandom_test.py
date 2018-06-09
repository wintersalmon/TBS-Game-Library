import collections

from mandom.data.events import EventCode, MandomEventFactory
from mandom.wrapper import MandomWrapper


def main():
    settings = {
        'player_names': ['player_{}'.format(i) for i in range(4)]
    }
    wrapper = MandomWrapper.create(**settings)
    events = [
        MandomEventFactory.create(EventCode.INIT_ROUND.value),

        MandomEventFactory.create(EventCode.TURN_DRAW.value, player=0),
        MandomEventFactory.create(EventCode.TURN_ADD_MONSTER_TO_DUNGEON.value, player=0),

        MandomEventFactory.create(EventCode.TURN_DRAW.value, player=1),
        MandomEventFactory.create(EventCode.TURN_ADD_MONSTER_TO_DUNGEON.value, player=1),

        MandomEventFactory.create(EventCode.TURN_DRAW.value, player=2),
        MandomEventFactory.create(EventCode.TURN_ADD_MONSTER_TO_DUNGEON.value, player=2),

        MandomEventFactory.create(EventCode.TURN_DRAW.value, player=3),
        MandomEventFactory.create(EventCode.TURN_ADD_MONSTER_TO_DUNGEON.value, player=3),

        MandomEventFactory.create(EventCode.TURN_DRAW.value, player=0),
        MandomEventFactory.create(EventCode.TURN_REMOVE_WEAPON_FROM_HERO.value, player=0, weapon=1),

        MandomEventFactory.create(EventCode.TURN_DRAW.value, player=1),
        MandomEventFactory.create(EventCode.TURN_REMOVE_WEAPON_FROM_HERO.value, player=1, weapon=3),

        MandomEventFactory.create(EventCode.TURN_DRAW.value, player=2),
        MandomEventFactory.create(EventCode.TURN_REMOVE_WEAPON_FROM_HERO.value, player=2, weapon=5),

        MandomEventFactory.create(EventCode.TURN_DRAW.value, player=3),
        MandomEventFactory.create(EventCode.TURN_REMOVE_WEAPON_FROM_HERO.value, player=3, weapon=6),

        MandomEventFactory.create(EventCode.TURN_FOLD.value, player=0),
        MandomEventFactory.create(EventCode.TURN_FOLD.value, player=1),
        MandomEventFactory.create(EventCode.TURN_FOLD.value, player=2),

        MandomEventFactory.create(EventCode.CHALLENGE_DUNGEON.value, player=3),
    ]
    records = collections.deque()

    draw(wrapper.game)
    for e in events:
        e.update(wrapper.game)
        print(e)
        draw(wrapper.game)
        records.append((e, wrapper.game.encode()))

    print('------------------------------')
    while records:
        e, data = records.pop()
        assert data == wrapper.game.encode()
        print(e)
        e.rollback(wrapper.game)
        draw(wrapper.game)


def draw_player(player):
    player_fmt = 'Player(name={name} vp={vp} lp={lp})'

    return player_fmt.format(
        name=player.name,
        vp=player.victory_point,
        lp=player.life_point,
    )


def draw(game):
    for p, player in enumerate(game.players):
        player_fmt = draw_player(player)
        if len(game.player_turn_tracker) and p == game.player_turn_tracker.current_player:
            player_fmt += ' *'
        print(player_fmt)

    print('weapons_enabled: {}'.format(game.hero.encode()['weapons']))
    print('weapons_disabled: {}'.format(game.removed_weapons.encode()['items']))
    print('monsters_deck: {}'.format(game.deck.encode()['cards']))
    print('monsters_dungeon: {}'.format(game.dungeon.encode()['items']))
    print('monsters_removed: {}'.format(game.removed_monsters.encode()['items']))
    print()


if __name__ == '__main__':
    main()
