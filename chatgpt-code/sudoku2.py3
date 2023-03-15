#!/usr/bin/env python3
def is_valid(board, row, col, num):
    # Check if the number is in the same row or column
    for i in range(4):
        if board[row][i] == num or board[i][col] == num:
            return False

    # Check if the number is in the same 2x2 subgrid
    start_row = row - row % 2
    start_col = col - col % 2
    for i in range(2):
        for j in range(2):
            if board[i + start_row][j + start_col] == num:
                return False

    return True

def solve_sudoku(board):
    row = -1
    col = -1
    empty = False
    for i in range(4):
        for j in range(4):
            if board[i][j] == 0:
                row = i
                col = j
                empty = True
                break
        if empty:
            break

    if not empty:
        return True

    for num in range(1, 5):
        if is_valid(board, row, col, num):
            board[row][col] = num
            if solve_sudoku(board):
                return True
            board[row][col] = 0

    return False

if __name__ == "__main__":
    sudoku = [
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

    if solve_sudoku(sudoku):
        for row in sudoku:
            print(row)
    else:
        print("No solution exists.")
