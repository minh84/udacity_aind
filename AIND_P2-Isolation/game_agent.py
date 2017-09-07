"""Finish all TODO items in this file to complete the isolation project, then
test your agent's strength against a set of known agents using tournament.py
and include the results in your report.
"""
import random
import numpy as np

class SearchTimeout(Exception):
    """Subclass base exception for code clarity. """
    pass

def weighted_score(game, player, weight):
    """The "Improved" evaluation function discussed in lecture that outputs a
    score equal to the difference in the number of moves available to the
    two players.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : hashable
        One of the objects registered by the game object as a valid player.
        (i.e., `player` should be either game.__player_1__ or
        game.__player_2__).

    Returns
    ----------
    float
        The heuristic value of the current game state
    """
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    # look ahead

    own_moves = len(game.get_legal_moves(player))
    opp_moves = len(game.get_legal_moves(game.get_opponent(player)))
    return float(own_moves - weight*opp_moves)

def custom_score(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    This should be the best heuristic function for your project submission.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    # TODO: finish this function!
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    # get percent occupied
    blank_spaces = game.get_blank_spaces()
    occupied = float(len(blank_spaces)) / (game.width * game.height)

    # look ahead
    own_moves = game.get_legal_moves(player)
    opp_moves = game.get_legal_moves(game.get_opponent(player))

    # invoke __get_moves from outside: https://www.python.org/dev/peps/pep-0008/
    own_next_moves = np.mean([len(game._Board__get_moves(m)) for m in own_moves])
    opp_next_moves = np.mean([len(game._Board__get_moves(m)) for m in opp_moves])

    return (1.0 - occupied) * (len(own_moves) - len(opp_moves)) + occupied * (own_next_moves - opp_next_moves)


def custom_score_2(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    # TODO: finish this function!
    return weighted_score(game, player, 1.5)


def custom_score_3(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    # TODO: finish this function!
    return weighted_score(game, player, 2.0)


class IsolationPlayer:
    """Base class for minimax and alphabeta agents -- this class is never
    constructed or tested directly.

    ********************  DO NOT MODIFY THIS CLASS  ********************

    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate sucessors of the
        current state.)

    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """
    def __init__(self, search_depth=3, score_fn=custom_score, timeout=10.):
        self.search_depth = search_depth
        self.score = score_fn
        self.time_left = None
        self.TIMER_THRESHOLD = timeout

    def check_time(self):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()


class MinimaxPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using depth-limited minimax
    search. You must finish and test this player to make sure it properly uses
    minimax to return a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        **************  YOU DO NOT NEED TO MODIFY THIS FUNCTION  *************

        For fixed-depth search, this function simply wraps the call to the
        minimax method, but this method provides a common interface for all
        Isolation agents, and you will replace it in the AlphaBetaPlayer with
        iterative deepening search.

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left

        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        best_move = (-1, -1)

        try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.
            return self.minimax(game, self.search_depth)

        except SearchTimeout:
            pass  # Handle any actions required after timeout as needed

        # Return the best move from the last completed search iteration
        return best_move

    def minimax(self, game, depth):
        """Implement depth-limited minimax search algorithm as described in
        the lectures.

        This should be a modified version of MINIMAX-DECISION in the AIMA text.
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Minimax-Decision.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """


        # TODO: finish this function!
        _, best_move = self.maxval(game, depth)
        return best_move

    def maxval(self, game, depth):
        """
        Implement the MAX-VALUE from https://github.com/aimacode/aima-pseudocode/blob/master/md/Minimax-Decision.md
        We modified so that we return heuristic evaluation if current search_depth reached fix-depth
        :param game:          current game board (state)
        :param depth:         depth to search (0 means stop)
        :return:
            a float (best score for all actions)
            a best move

        Note that function might throw error if time runs out
        """
        # check for time
        self.check_time()

        #player (self) try to maximize outcome
        player = self

        # if search_depth >= fixed depth => return evaluation function
        if depth == 0:
            return self.score(game, self), (-1, -1)

        # search next layer
        # if there is no legal moves then we lose => return -inf
        max_val  = float("-inf")
        max_move = (-1, -1)
        for m in game.get_legal_moves(player):
            v = self.minval(game.forecast_move(m), depth - 1)
            if v > max_val:
                max_val = v
                max_move = m

        return max_val, max_move

    def minval(self, game, depth):
        """
        Implement the MIN-VALUE from https://github.com/aimacode/aima-pseudocode/blob/master/md/Minimax-Decision.md
        We modified so that we return heuristic evaluation if current search_depth reached fix-depth
        :param game:          current game board (state)
        :param depth:         depth avail to search (0 means stop)
        :return:
            a float (worst score for all actions)
            a worst move
        """
        # check for time
        self.check_time()

        # evaluate utility
        player = game.get_opponent(self)    # opponent try to minimize outcome

        # if search_depth >= fixed depth => return evaluation function: always score with self
        if depth == 0:
            return self.score(game, self)

        # search next layer
        # if there is no legal moves then we win => return inf
        min_val = float("inf")
        for m in game.get_legal_moves(player):
            v, _ = self.maxval(game.forecast_move(m), depth - 1)
            if v < min_val:
                min_val = v

        return min_val

class AlphaBetaPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using iterative deepening minimax
    search with alpha-beta pruning. You must finish and test this player to
    make sure it returns a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        Modify the get_move() method from the MinimaxPlayer class to implement
        iterative deepening search instead of fixed-depth search.

        **********************************************************************
        NOTE: If time_left() < 0 when this function returns, the agent will
              forfeit the game due to timeout. You must return _before_ the
              timer reaches 0.
        **********************************************************************

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left

        # TODO: finish this function!
        depth = 0
        best_move = (-1, -1)
        while (True):
            try:
                depth += 1
                best_move = self.alphabeta(game, depth)
            except SearchTimeout:
                break

        return best_move

    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf")):
        """Implement depth-limited minimax search with alpha-beta pruning as
        described in the lectures.

        This should be a modified version of ALPHA-BETA-SEARCH in the AIMA text
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Alpha-Beta-Search.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        alpha : float
            Alpha limits the lower bound of search on minimizing layers

        beta : float
            Beta limits the upper bound of search on maximizing layers

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """

        # TODO: finish this function!
        # print('-------------------------------')
        # print('Game state')
        # print(game.to_string())
        # print('-------------------------------')
        _, best_move = self.maxval(game, depth, alpha, beta)
        # print(best_move)
        # print('-------------------------------\n')

        return best_move

    def maxval(self, game, depth, alpha, beta):
        self.check_time()

        # we try to maximize outcome
        player = self

        # if search_depth >= fixed depth => return evaluation function
        if depth == 0:
            return self.score(game, self), (-1, -1)

        # search next layer
        # if there is no legal moves then we lose => return -inf
        max_val = float("-inf")
        max_move = (-1, -1)
        for m in game.get_legal_moves(player):
            v = self.minval(game.forecast_move(m), depth - 1, alpha, beta)
            if v > max_val:
                max_val = v
                max_move = m

                if max_val >= beta:
                    return max_val, max_move

            alpha = max(alpha, max_val)

        return max_val, max_move

    def minval(self, game, depth, alpha, beta):
        self.check_time()

        # evaluate utility
        player = game.get_opponent(self)  # opponent try to minimize outcome

        # if search_depth >= fixed depth => return evaluation function: always score with self
        if depth == 0:
            return self.score(game, self)

        # search next layer
        # if there is no legal moves then we win => return inf
        min_val = float("inf")
        # print('\tLegal moves {}'.format(legal_moves))
        for m in game.get_legal_moves(player):
            v, _ = self.maxval(game.forecast_move(m), depth - 1, alpha, beta)
            if v < min_val:
                min_val = v
                if min_val <= alpha:
                    return  min_val

            beta = min(beta, min_val)

        # print('min val alpha-beta {}'.format(alpha_beta))
        return min_val

