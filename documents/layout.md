## CORE CLASS LAYOUT

### MODEL
- Game(Serializable)
    + get
    + set
    + has
    + encode
    + decode


- Event(Serializable)
    + create
    + update
    + rollback
    + encode
    + decode


### Manager
- GameManager(Serializable)
    + init
    + create
    + encode
    + decode


- GameViewableManager(GameManager)
    + view


- GameMutableManager(GameViewableManager)
    + update


- GameReplayManager(GameViewableManager)
    + max_position
    + get_position
    + set_position
    + forward
    + backward


- GameCLIManager(GameMutableManager)
    + status


### UTIL
- Serializable
    + encode
    + decode
