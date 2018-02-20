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
    - str


### Manager
- GameManger()
    + init(GameWrapper)
    - str


- GameUpdateManager(GameManager)
    + update
    - str

- GameReplayManager(GameManager)
    + max_position
    + get_position
    + set_position
    + forward
    + backward
    - str


### UTIL
- Serializable
    + encode
    + decode
