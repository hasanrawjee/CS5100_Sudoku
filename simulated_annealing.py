import random
import math
import numpy as np
import time


def initial_solution(board):
    # Create initial solution from the given board by filling empty cells randomly
    solution = np.copy(board)
    for i in range(9):
        numbers = list(range(1, 10))
        for j in range(9):
            if solution[i][j] == 0:
                random.shuffle(numbers)
                for number in numbers:
                    if is_valid_move(solution, i, j, number):
                        solution[i][j] = number
                        break
    return solution


def is_valid_move(board, row, col, number):
    # Check if a move is valid
    # Check row and column
    if number in board[row] or number in board[:, col]:
        return False

    # Check 3x3 square
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(start_row, start_row + 3):
        for j in range(start_col, start_col + 3):
            if board[i][j] == number:
                return False

    return True


def cost_function(board):
    # Calculate the cost of the current solution (lower is better)
    cost = 0
    for i in range(9):
        for j in range(9):
            if not is_valid_move(board, i, j, board[i][j]):
                cost += 1
    return cost


def get_neighbour(solution, board):
    # Get a neighboring solution by swapping two cells in a random row
    neighbour = np.copy(solution)

    # Find rows with at least two empty cells
    valid_rows = [
        i for i in range(9) if len([cell for cell in board[i] if cell == 0]) >= 2
    ]

    if valid_rows:
        row = random.choice(valid_rows)
        empty_cells = [i for i in range(9) if board[row][i] == 0]
        col1, col2 = random.sample(empty_cells, 2)
        neighbour[row][col1], neighbour[row][col2] = (
            neighbour[row][col2],
            neighbour[row][col1],
        )

    return neighbour


def simulated_annealing(board):
    # Solve Sudoku using Simulated Annealing
    current_solution = initial_solution(board)
    current_cost = cost_function(current_solution)
    temperature = 1.0
    cooling_rate = 0.99
    min_temperature = 0.01

    while temperature > min_temperature:
        neighbour = get_neighbour(current_solution, board)
        neighbour_cost = cost_function(neighbour)

        if neighbour_cost < current_cost or random.uniform(0, 1) < math.exp(
            (current_cost - neighbour_cost) / temperature
        ):
            current_solution = neighbour
            current_cost = neighbour_cost

        temperature *= cooling_rate

        if current_cost == 0:
            break

    return current_solution


# Uncomment below to run algorithm on hard sudoku problem
"""board = np.array(
    [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9],
    ]
)
start_time = time.time()
solution = simulated_annealing(board)
end_time = time.time()

for row in solution:
    print(" ".join(str(num) for num in row))
print(f"Time taken to solve: {end_time - start_time} seconds")"""

# Uncomment below to run algorithm on sudoku.csv (1 million numpy array pairs of Sudoku games)
"""quizzes = np.zeros((1000000, 81), np.int32)
for i, line in enumerate(open("sudoku.csv", "r").read().splitlines()[1:]):
    quiz, _ = line.split(",")
    quizzes[i] = [int(c) for c in quiz]
quizzes = quizzes.reshape((-1, 9, 9))

start_time = time.time()
for i in range(500000):
    puzzle = quizzes[i]
    solution = simulated_annealing(puzzle)
end_time = time.time()

print(f"Time taken to solve 500,000 Sudokus: {end_time - start_time} seconds")"""
