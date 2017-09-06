from sample_players import *
from game_agent import *
from isolation import Board
import timeit

def test_case1():
    player1 = MinimaxPlayer(search_depth=1, score_fn=open_move_score)
    player2 = GreedyPlayer()
    game = Board(player1, player2, 9, 9)
    game._board_state
    game._board_state = [0, 0, 0, 0, 0, 0, 0, 0, 0, \
                         0, 0, 0, 0, 0, 0, 0, 0, 0, \
                         0, 0, 1, 1, 0, 0, 1, 0, 0, \
                         0, 0, 0, 0, 1, 1, 0, 0, 0, \
                         0, 1, 0, 1, 1, 1, 0, 0, 0, \
                         0, 0, 1, 0, 1, 0, 0, 0, 0, \
                         0, 0, 1, 1, 1, 0, 0, 0, 0, \
                         0, 0, 0, 0, 0, 0, 0, 0, 0, \
                         0, 0, 0, 0, 0, 0, 0, 0, 0, \
                         0, 37, 57]
    print('Current game')
    print(game.to_string())
    print('Active player {}'.format(game.active_player))
    print('Legal moves\n\t{}'.format(game.get_legal_moves()))

    time_limit  = 10
    time_millis = lambda: 1000 * timeit.default_timer()
    move_start = time_millis()
    time_left = lambda: 20
    game_copy = game.copy()
    print('Next move: \n\t{}'.format(game.active_player.get_move(game_copy, time_left)))
    print('Expected move is (5,5), please verify!!!')

if __name__ == '__main__':
    test_case1()