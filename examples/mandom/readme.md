

## ALLOWED EVENTS FOR EACH STATUS

    GAME_INIT
        init_round_event (ROUND)

    ROUND
        challenge_dungeon (CHALLENGE or GAME_OVER)
        turn_fold (ROUND)
        turn_draw (TURN)

    TURN
        turn_add_monster_to_dungeon (ROUND)
        turn_remove_weapon_from_hero (ROUND)

    CHALLENGE
        init_round_event (ROUND)

    GAME_OVER


## EVENT UPDATE REQUIREMENTS

    init_round_event

    challenge_dungeon
        - event param player is current player
        - active player count == 1

    pass_turn
        - event param player is current player
        - active player count > 1

    turn_draw
        - event param player is current player
        - active player count > 1
        - deck is not empty

    turn_add_monster_to_dungeon
        - event param player is current player

    turn_remove_weapon_from_hero
        - event param player is current player
        - event param weapon in hero weapons
