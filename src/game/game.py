from .board import create_board, check_winner, deal_position, pick, \
                   GAME_CONTINUE, will_starve_player
from .renderer import render, render_score
from .constants import PIT_COUNT


def start(player_one, player_two):
    print("\n######### GAME STARTED ############\n")

    board = create_board(PIT_COUNT)
    print(render(board))

    players = [
        get_complement_properties_player(0, player_one),
        get_complement_properties_player(1, player_two)
      ]

    number_current_player = 0

    score = [0] * 2
    game_state = GAME_CONTINUE

    while game_state == GAME_CONTINUE:
        current_player = players[number_current_player]

        position = current_player['player'].get_position(board, current_player)
        if position < 0:
            print("Invalid position")
            continue

        board, score = play_turn(current_player, board, position, score)
        score, game_state = check_winner(current_player, board, position,
                                         game_state, score)
        number_current_player = 1 - number_current_player
        print(render(board))
        print(render_score(score))

    print("Winner player: " + game_state)


def get_complement_properties_player(number, player=None):
    half_pit = int(PIT_COUNT / 2)
    return {
        'number': number,
        'min_position': number * half_pit,
        'max_position': (1 + number) * half_pit,
        'min_pick': (1 - number) * half_pit,
        'max_pick': (2 - number) * half_pit,
        'player': player,
    }


def play_turn(current_player, board, position, score):
    starving, board, score = will_starve_player(current_player,
                                                board,
                                                position,
                                                score,
                                                )

    if starving:
        deal_position(board, position, score)
        return board, score
    else:
        return pick(current_player, board, position, score)
