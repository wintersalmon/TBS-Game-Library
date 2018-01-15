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


### Wrapper
- GameWrapper(Serializable)
    + init
    + create
    + encode
    + decode
    - repr


### Manager
- GameManger()
    + init(GameWrapper)
    - repr


- GameUpdateManager(GameManager)
    + update
    - repr

- GameReplayManager(GameManager)
    + max_position
    + get_position
    + set_position
    + forward
    + backward
    - repr


### UTIL
- Serializable
    + encode
    + decode
