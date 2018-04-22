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


- GameLoadManager(GameManager)
    + load(cls_wrapper, file_directory, file_name)


- GameSaveManager(GameLoadManager)
    + save(file_directory, file_name)


- GameUpdateManager(GameSaveManager)
    + update
    - str


- GameReplayManager(GameLoadManager)
    + max_position
    + get_position
    + set_position
    + forward
    + backward
    - str

### UI
- todo : work in progress

- UI()

- CLI()

- ReplayCLI()

- PlayCLI()


### UTIL
- Serializable
    + encode
    + decode
