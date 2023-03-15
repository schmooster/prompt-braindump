#!/usr/bin/env python3
import sys
import argparse
import random
import math
from copy import deepcopy


class Sudoku:
    def __init__(self, grid, N):
        self.grid = grid
        self.N = N
        self.box_size = int(math.sqrt(N))
        if N == 16:
            self.box_size = 4

    def is_row_safe(self, row, num):
        return num not in self.grid[row]

    def is_col_safe(self, col, num):
        return num not in [self.grid[row][col] for row in range(self.N)]

    def is_box_safe(self, row, col, num):
        start_row, start_col = row - row % self.box_size, col - col % self.box_size
        for i in range(self.box_size):
            for j in range(self.box_size):
                if self.grid[i + start_row][j + start_col] == num:
                    return False
        return True

    def is_safe(self, row, col, num):
        return (self.is_row_safe(row, num)
                and self.is_col_safe(col, num)
                and self.is_box_safe(row, col, num))

    def find_empty_cell(self):
        for row in range(self.N):
            for col in range(self.N):
                if self.grid[row][col] == 0:
                    return row, col
        return None

    def solve(self):
        empty_cell = self.find_empty_cell()
        if not empty_cell:
            return True

        row, col = empty_cell
        for num in range(1, self.N + 1):
            if self.is_safe(row, col, num):
                self.grid[row][col] = num
                if self.solve():
                    return True
                self.grid[row][col] = 0

        return False


def generate_puzzle(N, num_given_cells):
    grid = [[0] * N for _ in range(N)]
    sudoku = Sudoku(grid, N)

    for _ in range(num_given_cells):
        row, col = random.randint(0, N - 1), random.randint(0, N - 1)
        num = random.randint(1, N)
        while not sudoku.is_safe(row, col, num) or sudoku.grid[row][col] != 0:
            row, col = random.randint(0, N - 1), random.randint(0, N - 1)
            num = random.randint(1, N)

        sudoku.grid[row][col] = num

    return sudoku.grid


def print_grid(grid):
    for row in grid:
        print(row)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-g", "--generate", help="Generate a Sudoku puzzle", action="store_true")
    parser.add_argument("-s", "--solve", help="Solve a Sudoku puzzle from a file", type=str)
    parser.add_argument("-d", "--difficulty", help="Difficulty level (1-12)", type=int, default=5)
    parser.add_argument("-n", "--num_cells", help="Number of cells per side in a grid (default: 9)", type=int, default=9)
    args = parser.parse_args()

    N = args.num_cells

    if args.generate:
        num_given_cells = max(17, (N * N) - (args.difficulty * 6))
        grid = generate_puzzle(N, num_given_cells)
        print("Generated puzzle:")
        print_grid(grid)

    if args.solve:
        with open(args.solve, 'r') as file:
            grid = [list(map(int, line.strip().split(','))) for line in file.readlines()]
            N = len(grid)

        sudoku = Sudoku(grid, N)

        if sudoku.solve():
            print("Solution:")
            print_grid(sudoku.grid)
        else:
            print("No solution found.")


if __name__ == "__main__":
    main()
