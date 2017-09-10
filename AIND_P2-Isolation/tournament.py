"""Estimate the strength rating of a student defined heuristic by competing
against fixed-depth minimax and alpha-beta search agents in a round-robin
tournament.

NOTE: All agents are constructed from the student CustomPlayer implementation,
so any errors present in that class will affect the outcome.

The student agent plays a number of "fair" matches against each test agent.
The matches are fair because the board is initialized randomly for both
players, and the players play each match twice -- once as the first player and
once as the second player.  Randomizing the openings and switching the player
order corrects for imbalances due to both starting position and initiative.
"""
import itertools
import random
import warnings
import pickle
import sys
import time
from collections import namedtuple

from isolation import Board
from sample_players import (RandomPlayer, open_move_score,
                            improved_score, center_score)
from game_agent import (MinimaxPlayer, AlphaBetaPlayer, custom_score_adaptive, custom_score_comb,
                        custom_score_2, custom_score_3)

NUM_MATCHES = 50  # number of matches against each opponent
TIME_LIMIT = 150  # number of milliseconds before timeout

DESCRIPTION = """
This script evaluates the performance of the custom_score evaluation
function against a baseline agent using alpha-beta search and iterative
deepening (ID) called `AB_Improved`. The three `AB_Custom` agents use
ID and alpha-beta search with the custom_score functions defined in
game_agent.py.
"""

Agent = namedtuple("Agent", ["player", "name"])


def play_round(cpu_agent, test_agents, win_counts, num_matches):
    """Compare the test agents to the cpu agent in "fair" matches.

    "Fair" matches use random starting locations and force the agents to
    play as both first and second player to control for advantages resulting
    from choosing better opening moves or having first initiative to move.
    """
    timeout_count = 0
    forfeit_count = 0
    for _ in range(num_matches):

        games = sum([[Board(cpu_agent.player, agent.player),
                      Board(agent.player, cpu_agent.player)]
                    for agent in test_agents], [])

        # initialize all games with a random move and response
        for _ in range(2):
            move = random.choice(games[0].get_legal_moves())
            for game in games:
                game.apply_move(move)

        # play all games and tally the results
        for game in games:
            winner, hist, termination = game.play(time_limit=TIME_LIMIT)
            win_counts[winner] += 1

            if termination == "timeout":
                timeout_count += 1
            elif termination == "forfeit":
                forfeit_count += 1
                # dbg_dict = {'hist'            : hist,
                #             'board'           : game._board_state,
                #             'player1'         : type(game._player_1),
                #             'player2'         : type(game._player_2)}
                # with open('dbg.pkl', 'wb') as f:
                #     pickle.dump(dbg_dict, f)
                #     print('Debug info is dumped to {}'.format('dbg.pkl'))
                #
                # sys.exit(0)

    return timeout_count, forfeit_count


def update(total_wins, wins):
    for player in total_wins:
        total_wins[player] += wins[player]
    return total_wins


def play_matches(cpu_agents, test_agents, num_matches):
    """Play matches between the test agent and each cpu_agent individually. """
    total_wins = {agent.player: 0 for agent in test_agents}
    total_timeouts = 0.
    total_forfeits = 0.
    total_matches = 2 * num_matches * len(cpu_agents)

    print("\n{:^9}{:^15}".format("Match #", "Opponent") + ''.join(['{:^15}'.format(x[1].name) for x in enumerate(test_agents)]))
    print("{:^9}{:^15} ".format("", "") +  ' '.join(['{:^6}| {:^6}'.format("Won", "Lost") for x in enumerate(test_agents)]))

    for idx, agent in enumerate(cpu_agents):
        wins = {key: 0 for (key, value) in test_agents}
        wins[agent.player] = 0

        print("{!s:^9}{:^15}".format(idx + 1, agent.name), end="", flush=True)

        counts = play_round(agent, test_agents, wins, num_matches)
        total_timeouts += counts[0]
        total_forfeits += counts[1]
        total_wins = update(total_wins, wins)
        _total = 2 * num_matches
        round_totals = sum([[wins[agent.player], _total - wins[agent.player]]
                            for agent in test_agents], [])
        print(' ' + ' '.join([
            '{:^6}| {:^6}'.format(
                round_totals[i],round_totals[i+1]
            ) for i in range(0, len(round_totals), 2)
        ]))

    print("-" * 74)
    print('{:^9}{:^15}'.format("", "Win Rate:") +
        ''.join([
            '{:^15}'.format(
                "{:.1f}%".format(100 * total_wins[x[1].player] / total_matches)
            ) for x in enumerate(test_agents)
    ]))

    if total_timeouts:
        print(("\nThere were {} timeouts during the tournament -- make sure " +
               "your agent handles search timeout correctly, and consider " +
               "increasing the timeout margin for your agent.\n").format(
            total_timeouts))
    if total_forfeits:
        print(("\nYour ID search forfeited {} games while there were still " +
               "legal moves available to play.\n").format(total_forfeits))

def test_aggresive():
    custom_score_2_0_5 = lambda game, player: custom_score_2(game, player, 0.5)
    custom_score_2_1_5 = lambda game, player: custom_score_2(game, player, 1.5)
    custom_score_2_2_0 = lambda game, player: custom_score_2(game, player, 2.0)

    test_agents = [
        Agent(AlphaBetaPlayer(score_fn=improved_score),     "AB_Improved"),
        Agent(AlphaBetaPlayer(score_fn=custom_score_2_0_5), "AB_Aggr_0.5"),
        Agent(AlphaBetaPlayer(score_fn=custom_score_2_1_5), "AB_Aggr_1.5"),
        Agent(AlphaBetaPlayer(score_fn=custom_score_2_2_0), "AB_Aggr_2.0"),
    ]
    return test_agents

def test_weighted_move():
    custom_score_3_0_5 = lambda game, player: custom_score_3(game, player, 0.5)
    custom_score_3_1_0 = lambda game, player: custom_score_3(game, player, 1.0)
    custom_score_3_1_5 = lambda game, player: custom_score_3(game, player, 1.5)
    custom_score_3_2_0 = lambda game, player: custom_score_3(game, player, 2.0)

    test_agents = [
        Agent(AlphaBetaPlayer(score_fn=improved_score), "AB_Improved")
       ,Agent(AlphaBetaPlayer(score_fn=custom_score_3_0_5), "AB_Wm_0.5")
       ,Agent(AlphaBetaPlayer(score_fn=custom_score_3_1_0), "AB_Wm_1.0")
       ,Agent(AlphaBetaPlayer(score_fn=custom_score_3_1_5), "AB_Wm_1.5")
       ,Agent(AlphaBetaPlayer(score_fn=custom_score_3_2_0), "AB_Wm_2.0")
    ]

    return test_agents

def test_combined_strategy():
    custom_score_1_0_5 = lambda game, player: custom_score_comb(game, player, 0.5)
    custom_score_1_1_0 = lambda game, player: custom_score_comb(game, player, 1.5)
    custom_score_1_2_0 = lambda game, player: custom_score_comb(game, player, 2.0)

    test_agents = [
          Agent(AlphaBetaPlayer(score_fn=improved_score), "AB_Improved")
        , Agent(AlphaBetaPlayer(score_fn=custom_score_1_0_5), "AB_Comb_0.5")
        , Agent(AlphaBetaPlayer(score_fn=custom_score_1_1_0), "AB_Comb_1.0")
        , Agent(AlphaBetaPlayer(score_fn=custom_score_1_2_0), "AB_Comb_2.0")
    ]

    return test_agents

def test_combined_adaptive():
    custom_score_adaptive_0 = lambda game, player: custom_score_adaptive(game, player, True)
    custom_score_adaptive_1 = lambda game, player: custom_score_adaptive(game, player, False)

    test_agents = [
          Agent(AlphaBetaPlayer(score_fn=improved_score), "AB_Improved")
        , Agent(AlphaBetaPlayer(score_fn=custom_score_adaptive_0), "AB_Comb_Occ")
        , Agent(AlphaBetaPlayer(score_fn=custom_score_adaptive_1), "AB_Comb_1-Occ")
    ]

    return test_agents

def main():

    # Define two agents to compare -- these agents will play from the same
    # starting position against the same adversaries in the tournament
    test_agents = test_combined_strategy()

    # Define a collection of agents to compete against the test agents
    cpu_agents = [
        Agent(RandomPlayer(), "Random"),
        Agent(MinimaxPlayer(score_fn=open_move_score), "MM_Open"),
        Agent(MinimaxPlayer(score_fn=center_score), "MM_Center"),
        Agent(MinimaxPlayer(score_fn=improved_score), "MM_Improved"),
        Agent(AlphaBetaPlayer(score_fn=open_move_score), "AB_Open"),
        Agent(AlphaBetaPlayer(score_fn=center_score), "AB_Center"),
        Agent(AlphaBetaPlayer(score_fn=improved_score), "AB_Improved")
    ]

    print(DESCRIPTION)
    print("{:^74}".format("*************************"))
    print("{:^74}".format("Playing Matches"))
    print("{:^74}".format("*************************"))
    play_matches(cpu_agents, test_agents, NUM_MATCHES)


if __name__ == "__main__":
    ts = time.time()
    main()
    te = time.time()
    print('Your total run-time {:.2f}'.format(te - ts))
