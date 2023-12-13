import numpy as np
import time


def cross(A, B):
    # Cross product of elements in A and elements in B.
    return [a + b for a in A for b in B]


digits = "123456789"
rows = "ABCDEFGHI"
cols = digits
squares = cross(rows, cols)
unitlist = (
    [cross(rows, c) for c in cols]
    + [cross(r, cols) for r in rows]
    + [cross(rs, cs) for rs in ("ABC", "DEF", "GHI") for cs in ("123", "456", "789")]
)
units = dict((s, [u for u in unitlist if s in u]) for s in squares)
peers = dict((s, set(sum(units[s], [])) - set([s])) for s in squares)


def parse_grid(grid):
    # Convert grid to a dict of possible values, {square: digits}, or return False if a contradiction is detected.
    values = dict((s, digits) for s in squares)
    for s, d in grid_values(grid).items():
        if d in digits and not assign(values, s, d):
            return False
    return values


def grid_values(grid):
    # Convert grid into a dict of {square: char} with '0' or '.' for empties.
    chars = [c if c in digits or c in "0." else "0" for c in "".join(grid)]
    return dict(zip(squares, chars))


def assign(values, s, d):
    # Eliminate all the other values (except d) from values[s] and propagate.
    other_values = values[s].replace(d, "")
    if all(eliminate(values, s, d2) for d2 in other_values):
        return values
    else:
        return False


def eliminate(values, s, d):
    # Eliminate d from values[s]; propagate when values or places <= 2.
    if d not in values[s]:
        return values
    values[s] = values[s].replace(d, "")
    if len(values[s]) == 0:
        return False
    elif len(values[s]) == 1:
        d2 = values[s]
        if not all(eliminate(values, s2, d2) for s2 in peers[s]):
            return False
    for u in units[s]:
        dplaces = [s for s in u if d in values[s]]
        if len(dplaces) == 0:
            return False
        elif len(dplaces) == 1:
            if not assign(values, dplaces[0], d):
                return False
    return values


def display(values):
    pass


def solve(grid):
    values = parse_grid(grid)
    display(values)


# Uncomment below to run algorithm on hard sudoku problem

"""board = [
    "53..7....",
    "6..195...",
    ".98....6.",
    "8...6...3",
    "4..8.3..1",
    "7...2...6",
    ".6....28.",
    "...419..5",
    "....8..79",
]
start_time = time.time()
solve(board)
end_time = time.time()
print(f"Total time taken to solve: {end_time - start_time} seconds")"""
# Uncomment below to run algorithm on sudoku.csv (1 million numpy array pairs of Sudoku games)
"""quizzes = np.zeros((1000000, 81), np.int32)
solutions = np.zeros((1000000, 81), np.int32)
for i, line in enumerate(open("sudoku.csv", "r").read().splitlines()[1:]):
    quiz, solution = line.split(",")
    for j, q_s in enumerate(zip(quiz, solution)):
        q, s = q_s
        quizzes[i, j] = q
        solutions[i, j] = s
quizzes = quizzes.reshape((-1, 9, 9))

start_time = time.time()
for i in range(len(quizzes)):
    puzzle = quizzes[i]
    puzzle_string = "".join(str(num) for row in puzzle for num in row)
    puzzle_string = puzzle_string.replace("0", ".")
    solve(puzzle_string)  # Assuming your function prints the solution
end_time = time.time()
print(f"Time taken to solve 1,000,000 Sudokus: {end_time - start_time} seconds")"""
