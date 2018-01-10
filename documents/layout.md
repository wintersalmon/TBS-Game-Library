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


- GameMutableManager(GameManager)
    + update


- GameReplayManager(GameManager)
    + max_position
    + get_position
    + set_position
    + forward
    + backward


- GameCLIManager(GameMutableManager)
    + status
    + draw


### UTIL
- Serializable
    + encode
    + decode
