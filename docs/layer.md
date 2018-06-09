## Class Layer

### Tier 0
- save.json   # represents actual save file


### Tier 1
- data   # represents game objects
    + get
    + set
    + encode
    + decode
- event  # represents game actions
    + update
    + rollback
    + create
    + encode
    + decode
- status # uses data to represent game status, limits invalid events
    + get


### Tier 2
- represents actual game
- basic game functions
- Wrapper
    + encode
    + decode
    + create
    + push(e)
    + pop(): e


### Tier 3
- advanced game functions
- FileManager
- ReplayManager
- UpdateManager
- NetworkManager  # TBD


### Tier 4
- final layer of the system
- handles user interactions with game
