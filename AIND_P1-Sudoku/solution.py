from collections import defaultdict

assignments = []

def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [s + t for s in A for t in B]

# define some global variables
ROWS = 'ABCDEFGHI'
COLS = '123456789'

BOXES = cross(ROWS, COLS)

ROW_UNITs    = [cross(r, COLS) for r in ROWS]
COL_UNITs = [cross(ROWS, c) for c in COLS]
SQR_UNITs = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]

# add diagonal unit
DIG_UNITs = [[ROWS[i]+COLS[i] for i in range(9)], [ROWS[i]+COLS[8-i] for i in range(9)]]
UNITLIST  = ROW_UNITs + COL_UNITs + SQR_UNITs + DIG_UNITs

# map each cell -> related cell (same units)
UNITs = dict((s, [u for u in UNITLIST if s in u]) for s in BOXES)
PEERs = dict((s, set(sum(UNITs[s],[]))-set([s])) for s in BOXES)

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """

    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values

    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """

    # Find all instances of naked twins
    # Eliminate the naked twins as possibilities for their peers
    values = values.copy()

    naked_twins_cells = []
    for unit in UNITLIST:
        # find naked twins in this units
        naked_twins_unit = {}
        twins_unit = []
        for box in unit:
            v = values[box]
            if len(v) == 2:
                if v in naked_twins_unit:
                    twins_unit.append([naked_twins_unit[v], box])
                else:
                    naked_twins_unit[v] = box

        # eliminate the naked twins for other peers
        for cells in twins_unit:
            twin_val = values[cells[0]]

            for peer in set(unit) - set(cells):
                if len(values[peer]) > 1:
                    new_val = values[peer]
                    for v in twin_val:
                        new_val = new_val.replace(v, '')
                    assign_value(values, peer, new_val)

    return values

def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    empty_val = '123456789'
    retval = {}
    for i, box in enumerate(BOXES):
        if grid[i] == '.':
            retval[box] = empty_val
        else:
            retval[box] = grid[i]
    return retval

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1 + max(len(values[s]) for s in BOXES)
    line = '+'.join(['-' * (width * 3)] * 3)
    for r in ROWS:
        print(''.join(values[r + c].center(width) + ('|' if c in '36' else '')
                      for c in COLS))
        if r in 'CF': print(line)
    return

def eliminate(values):
    """
        Go through all the boxes, and whenever there is a box with a value, eliminate this value from the values of all its peers.
        Input: A sudoku in dictionary form.
        Output: The resulting sudoku in dictionary form.
    """
    # store cells that has explicit value
    values = values.copy()
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        for peer in PEERs[box]:
            new_val = values[peer].replace(digit, '')
            assign_value(values, peer, new_val)
    return values

def only_choice(values):
    """
        Go through all the units, and whenever there is a unit with a value that only fits in one box, assign the value to this box.
        Input: A sudoku in dictionary form.
        Output: The resulting sudoku in dictionary form.
    """
    values = values.copy()
    for unit in UNITLIST:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                assign_value(values, dplaces[0], digit)
    return values

def reduce_puzzle(values):
    """
        Iterate eliminate() and only_choice(). If at some point, there is a box with no available values, return False.
        If the sudoku is solved, return the sudoku.
        If after an iteration of both functions, the sudoku remains the same, return the sudoku.
        Input: A sudoku in dictionary form.
        Output: The resulting sudoku in dictionary form.
    """
    stalled = False
    while not stalled:
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        values = eliminate(values)
        values = only_choice(values)
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        stalled = solved_values_before == solved_values_after
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def search(values):
    "Using depth-first search and propagation, try all possible values."
    # First, reduce the puzzle using the previous function

    values = reduce_puzzle(values)

    if values is False:
        return False  ## Failed earlier (in reduce_puzzle)

    if all(len(values[s]) == 1 for s in BOXES):
        return values  ## Solved!

    # Choose one of the unfilled squares with the fewest possibilities
    n, s = min((len(values[s]), s) for s in BOXES if len(values[s]) > 1)
    # Now use recurrence to solve each one of the resulting sudokus, and
    for value in values[s]:
        new_sudoku = values.copy()
        assign_value(new_sudoku, s, value)
        attempt = search(new_sudoku)
        if attempt:
            return attempt

    return False

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    values = grid_values(grid)
    return search(values)

if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
