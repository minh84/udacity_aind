import copy

xlim = 3
ylim = 2


class GameState:
    def __init__(self):
        self._player = 0
        self._location = [None, None]

        # _board = 1 means not used yet
        self._board = []
        for i in range(xlim):
            self._board.append([1] * ylim)

        self._board[-1][-1] = 0

    def forecast_move(self, move):
        """ Return a new board object with the specified move
        applied to the current game state.

        Parameters
        ----------
        move: tuple
            The target position for the active player's next move
        """
        if move not in self.get_legal_moves():
            raise RuntimeError("Attempted forecast of illegal move")

        newBoard = copy.deepcopy(self)
        newBoard._location[newBoard._player] = move
        newBoard._board[move[0]][move[1]] = 0
        newBoard._player ^= 1
        return newBoard

    def get_legal_moves(self):
        """ Return a list of all legal moves available to the
        active player.  Each player should get a list of all
        empty spaces on the board on their first move, and
        otherwise they should get a list of all open spaces
        in a straight line along any row, column or diagonal
        from their current position. (Players CANNOT move
        through obstacles or blocked squares.) Moves should
        be a pair of integers in (column, row) order specifying
        the zero-indexed coordinates on the board.
        """

        # print(self._location)

        moves = []
        # first move anywhere not blocked yet
        if self._location[self._player] is None:
            for x in range(xlim):
                for y in range(ylim):
                    if self._board[x][y] == 1:
                        moves.append((x, y))
        else:
            # horizontal, then vertical, then diagonal 1, diagonal 2
            rays = [ (1, 0),   (-1, 0)
                    ,(0, 1),   (0, -1)
                    ,(1, -1),  (-1, 1)
                    ,(-1, -1), (1, 1)]
            for dx, dy in rays:
                _x, _y = self._location[self._player]
                while 0 <= _x + dx < xlim and 0 <= _y + dy < ylim:
                    _x, _y = _x + dx, _y + dy
                    if self._board[_x][_y] == 0:  # get blocked
                        break
                    moves.append((_x, _y))

        return moves