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


### MANAGER
- GameManager(Serializable)
    + update
    + create
    + encode
    + decode


### Wrappers
- GameWrapper(object)
    + init(game_controller)


- GameFileWrapper(GameManager)
    + save
    + load


- GameCLIWrapper(GameManager)
    + status
    + draw
    + (get_user_input)


- GameGUIWrapper(GameManager)
    + status
    + draw
    + (get_user_input)


- GameReplayWrapper(GameManager)
    + load
    + forward
    + backward
    + move_to


### UTIL
- Serializable
    + encode
    + decode
