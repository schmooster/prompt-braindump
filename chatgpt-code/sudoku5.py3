#!/usr/bin/env python3
import argparse
import random
from random import sample

class Sudoku:
    def __init__(self, grid):
        self.grid = grid

    def find_empty(self):
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                if self.grid[i][j] == 0:
                    return i, j
        return None

    def valid(self, num, pos):
        # Check row
        for i in range(len(self.grid[0])):
            if self.grid[pos[0]][i] == num and pos[1] != i:
                return False

        # Check column
        for i in range(len(self.grid)):
            if self.grid[i][pos[1]] == num and pos[0] != i:
                return False

        # Check box
        box_x = pos[1] // 3
        box_y = pos[0] // 3
        for i in range(box_y * 3, box_y * 3 + 3):
            for j in range(box_x * 3, box_x * 3 + 3):
                if self.grid[i][j] == num and (i, j) != pos:
                    return False
        return True

    def solve(self):
        find = self.find_empty()
        if not find:
            return self.grid

        row, col = find
        for i in range(1, 10):
            if self.valid(i, (row, col)):
                self.grid[row][col] = i
                if self.solve():
                    return self.grid
                self.grid[row][col] = 0
        return None

def generate_puzzle(N, num_given_cells):
    base = int(N**0.5)
    pattern = range(1, N + 1)
    puzzle = [[pattern[(base * (row % base) + row // base + col) % N] for col in range(N)] for row in range(N)]

    rows = random.sample(range(N), N)
    cols = random.sample(range(N), N)
    puzzle = [[puzzle[row][col] for col in cols] for row in rows]

    square_cells = random.sample(range(N * N), num_given_cells)
    for row in range(N):
        for col in range(N):
            if col not in square_cells:
                puzzle[row][col] = 0
    return puzzle

def main():
    parser = argparse.ArgumentParser(description="Sudoku Solver and Generator")
    parser.add_argument("-g", "--generate", action="store_true", help="generate a new puzzle")
    parser.add_argument("-s", "--solve", action="store_true", help="solve an existing puzzle")
    parser.add_argument("-d", "--difficulty", type=int, help="puzzle difficulty level (1-12)")
    parser.add_argument("-n", "--num_cells", type=int, default=9, help="number of cells per side (default: 9)")
    args = parser.parse_args()

    N = args.num_cells

    if args.solve:
        print("Enter the puzzle to solve (row by row, with 0 for empty cells):")
        grid = [list(map(int, input().split())) for _ in range(N)]
        sudoku = Sudoku(grid)
        solution = sudoku.solve()
        if solution:
            print("Solution:")
            for row in solution:
                print(row)
        else:
            print("No solution found.")
    elif args.generate:
        num_given_cells = N * N // 2
        if args.difficulty:
            num_given_cells -= (args.difficulty - 1) * N // 2

        grid = generate_puzzle(N, num_given_cells)
        print("Generated puzzle:")
        for row in grid:
            print(row)
    else:
        print("Please use -g/--generate or -s/--solve flag.")

if __name__ == "__main__":
    main()
