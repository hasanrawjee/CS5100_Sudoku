import numpy as np
import time


def is_valid(board, row, col, num):
    # Check if the number is not repeated in row, column and 3x3 subgrid
    for x in range(9):
        if (
            board[row][x] == num
            or board[x][col] == num
            or board[3 * (row // 3) + x // 3][3 * (col // 3) + x % 3] == num
        ):
            return False
    return True


def solve_sudoku(board):
    empty = find_empty_location(board)
    if not empty:
        return True  # No empty space left, puzzle solved
    row, col = empty

    for num in range(1, 10):
        if is_valid(board, row, col, num):
            board[row][col] = num
            if solve_sudoku(board):
                return True
            board[row][col] = 0  # Reset the cell for backtracking

    return False


def find_empty_location(board):
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == 0:
                return i, j
    return None


# Uncomment below to run algorithm on hard sudoku problem

"""board = [
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
start_time = time.time()

if solve_sudoku(board):
    for i in range(9):
        for j in range(9):
            print(board[i][j], end=" ")
        print()
else:
    print("No solution exists")
end_time = time.time()
print(f"Time taken to solve: {end_time - start_time} seconds")"""

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
solutions = solutions.reshape((-1, 9, 9))

start_time = time.time()
for i in range(len(quizzes)):
    puzzle = quizzes[i]
    solve_sudoku(puzzle)
end_time = time.time()

print(f"Time taken to solve 1,000,000 Sudokus: {end_time - start_time} seconds")"""
