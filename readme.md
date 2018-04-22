### Overview
+ TBS is Short For 'Turn Based Strategy'


### Purpose
+ The major Purpose of this project is to experiment different ways of creating TBS-Game and finding the best one
+ Another purpose is to collect commonly used TBS-Game-Components and create a core library


### Contents
    /docs
    /example  # need to be source root
        /chess
        /othello
        /tictactoe
            /data
                /events
                /status
            /wrapper.py
            /manager.py
            /main.py
    /tbs  # need to be source root
    readme.md


### How To Run

- `/tbs` must be Sources Root
- `/example` must be Sources Root

``` bash
cd examples

main.py play <package> [--cli]    # create new game
main.py replay <package> [--cli]  # load saved game in replay mode
# --cli: load game in CLI(command line interface) mode
```
