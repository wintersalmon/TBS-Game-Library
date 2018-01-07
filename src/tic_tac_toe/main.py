from tic_tac_toe.events import PlayerPlacementEvent
from tic_tac_toe.manager import TicTacToeManager


def main():
    settings = {
        'init_data': {
            'player_one': 'tom',
            'player_two': 'jerry',
            'rows': 3,
            'cols': 3
        }
    }
    tic_tac_toe_manager = TicTacToeManager.create(**settings)

    tic_tac_toe_manager.draw()
    while tic_tac_toe_manager:
        try:
            event = read_user_event(tic_tac_toe_manager.game.get_turn_player_name())
            tic_tac_toe_manager.update(event)
        except ValueError as e:
            print(e)
        except EOFError as e:
            print(e)
            break
        else:
            tic_tac_toe_manager.draw()

    en = tic_tac_toe_manager.encode()
    de = TicTacToeManager.decode(**en)
    de.draw()


def read_user_event(turn_player_name):
    row, col = input('row, col: ').split()
    row, col = int(row), int(col)

    if row == 0 and col == 0:
        raise EOFError

    row, col = row - 1, col - 1
    event = PlayerPlacementEvent.create(player_name=turn_player_name, row=row, col=col)

    return event


if __name__ == '__main__':
    main()
