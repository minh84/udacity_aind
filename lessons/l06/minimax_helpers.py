
def terminal_test(gameState):
    """ Return True if the game is over for the active player
    and False otherwise.
    """
    return len(gameState.get_legal_moves()) == 0


def min_value(gameState):
    """ Return the value for a win (+1) if the game is over,
    otherwise return the minimum value over all legal child
    nodes.
    """
    if terminal_test(gameState):
        return 1

    min_val = float("inf")
    for m in gameState.get_legal_moves():
        g = gameState.forecast_move(m)
        min_val = min(min_val, max_value(g))
    return min_val

def max_value(gameState):
    """ Return the value for a loss (-1) if the game is over,
    otherwise return the maximum value over all legal child
    nodes.
    """
    if terminal_test(gameState):
        return -1

    max_val = float("-inf")

    for m in gameState.get_legal_moves():
        g = gameState.forecast_move(m)
        min_val = max(max_val, min_value(g))
    return min_val


# This solution does the same thing using the built-in `max` function
# Note that "lambda" expressions are Python's version of anonymous functions
def minimax_decision(gameState):
    """ Return the move along a branch of the game tree that
    has the best possible value.  A move is a pair of coordinates
    in (column, row) order corresponding to a legal move for
    the searching player.

    You can ignore the special case of calling this function
    from a terminal state.
    """
    # The built in `max()` function can be used as argmax!
    return max(gameState.get_legal_moves(),
               key=lambda m: min_value(gameState.forecast_move(m)))
