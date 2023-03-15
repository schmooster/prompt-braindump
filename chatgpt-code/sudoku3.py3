#!/usr/bin/env python3

def is_valid(puzzle, row, col, num):
    for i in range(9):
        if puzzle[row][i] == num or puzzle[i][col] == num:
            return False

    start_row, start_col = row - row % 3, col - col % 3
    for i in range(3):
        for j in range(3):
            if puzzle[i + start_row][j + start_col] == num:
                return False

    return True

def solve(puzzle):
    row = col = -1
    empty = False
    for i in range(9):
        for j in range(9):
            if puzzle[i][j] == 0:
                row, col = i, j
                empty = True
                break
        if empty:
            break

    if not empty:
        return True

    for num in range(1, 10):
        if is_valid(puzzle, row, col, num):
            puzzle[row][col] = num
            if solve(puzzle):
                return True
            puzzle[row][col] = 0

    return False

sudoku_puzzle = [
    [0, 0, 0, 0, 0, 0, 0, 1, 2],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [3, 4, 5, 0, 0, 0, 0, 0, 0]
]

if solve(sudoku_puzzle):
    for row in sudoku_puzzle:
        print(row)
else:
    print("No solution exists.")
