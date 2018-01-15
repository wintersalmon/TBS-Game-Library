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
    + view


### Manager
- GameManger()
    + init(GameWrapper)


- GameUpdateManager(GameManager)
    + update


- GameReplayManager(GameManager)
    + max_position
    + get_position
    + set_position
    + forward
    + backward



### UTIL
- Serializable
    + encode
    + decode
