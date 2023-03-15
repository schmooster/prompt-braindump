#!/usr/bin/env python3

import sys
import math
import random
import argparse

from pathlib import Path
from multiprocessing import Pool
from functools import partial

class Sudoku:
    def __init__(self, grid):
        self.grid = grid
        self.N = len(grid)


    def is_safe(self, row, col, num):
        return (self.is_row_safe(row, num)
                and self.is_col_safe(col, num)
                and self.is_box_safe(row, col, num))

    def is_row_safe(self, row, num):
        return num not in self.grid[row]

    def is_col_safe(self, col, num):
        return num not in [self.grid[row][col] for row in range(len(self.grid))]

    def is_box_safe(self, row, col, num):
        box_size = int(len(self.grid)**0.5)
        start_row = row - row % box_size
        start_col = col - col % box_size

        for i in range(box_size):
            for j in range(box_size):
                if self.grid[i + start_row][j + start_col] == num:
                    return False
        return True

    def is_solved(self):
        for row in range(len(self.grid)):
            for col in range(len(self.grid)):
                if self.grid[row][col] == 0:
                    return False
        return True

    def solve(self):
        def solve_helper(row, col):
            if row == len(self.grid):
                return True

            if self.grid[row][col] != 0:
                return solve_helper(row + (col + 1) // len(self.grid), (col + 1) % len(self.grid))

            for num in range(1, len(self.grid) + 1):
                if self.is_safe(row, col, num):
                    self.grid[row][col] = num

                    if solve_helper(row + (col + 1) // len(self.grid), (col + 1) % len(self.grid)):
                        return True

                    self.grid[row][col] = 0

            return False

        return solve_helper(0, 0)

    def find_unassigned_cell(self):
        for row in range(self.N):
            for col in range(self.N):
                if self.grid[row][col] == 0:
                    return row, col
        return -1, -1  # No unassigned cell found

    def has_unique_solution(self):
        solutions = []
        self.find_all_solutions(solutions, 2)
        return len(solutions) == 1

    def find_all_solutions(self, solutions, max_solutions):
        if len(solutions) >= max_solutions:
            return

        row, col = self.find_unassigned_cell()
        if row == -1 and col == -1:
            solutions.append(self.grid)
            return

        for num in range(1, self.N + 1):
            if self.is_safe(row, col, num):
                self.grid[row][col] = num
                self.find_all_solutions(solutions, max_solutions)
                self.grid[row][col] = 0

def generate_solved_puzzle(N):
    grid = [[0] * N for _ in range(N)]
    sudoku = Sudoku(grid)
    
    def fill_grid(sudoku, row=0, col=0):
        if row == N - 1 and col == N:
            return True

        if col == N:
            row += 1
            col = 0

        if sudoku.grid[row][col] != 0:
            return fill_grid(sudoku, row, col + 1)

        nums = list(range(1, N + 1))
        random.shuffle(nums)

        for num in nums:
            if sudoku.is_safe(row, col, num):
                sudoku.grid[row][col] = num

                if fill_grid(sudoku, row, col + 1):
                    return True

        sudoku.grid[row][col] = 0
        return False

    if not fill_grid(sudoku):
        raise RuntimeError("Failed to generate a solved puzzle.")

    return sudoku.grid

def generate_puzzle(N, num_given_cells):
    solved_grid = generate_solved_puzzle(N)
    sudoku = Sudoku(solved_grid)

    # Remove random cells to create a puzzle
    remaining_cells = N * N - num_given_cells
    while remaining_cells > 0:
        row = random.randrange(N)
        col = random.randrange(N)
        if sudoku.grid[row][col] != 0:
            sudoku.grid[row][col] = 0
            remaining_cells -= 1

    return sudoku.grid

def read_grid_from_file(filename):
    with open(filename, 'r') as f:
        grid = [[(int(num) if num != 'X' else 0) for num in line.strip().split()] for line in f]
    return grid


def print_grid(grid):
    for row in grid:
        for num in row:
            print(num if num != 0 else 'X', end=' ')
        print()

def difficulty_to_num_given_cells(N, difficulty):
    min_given_cells = math.ceil(N * math.sqrt(N) / 2)
    max_given_cells = math.ceil(N * (N - math.sqrt(N)))
    range_given_cells = max_given_cells - min_given_cells
    num_given_cells = min_given_cells + round(difficulty / 10 * range_given_cells)
    return num_given_cells

def main():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-g', '--generate', action='store_true', help='Generate a puzzle')
    group.add_argument('-s', '--solve', metavar='FILENAME', help='Solve a puzzle from a file')
    parser.add_argument('-d', '--difficulty', type=int, choices=range(1, 11), default=5, help='Difficulty level (1-10)')
    parser.add_argument('-n', '--num_cells', type=int, help='Number of cells for the grid')
    args = parser.parse_args()

    if args.num_cells:
        N = args.num_cells
        if N != int(math.sqrt(N))**2:
            print("Error: The number of cells must have an integer square root.")
            sys.exit(1)
    else:
        N = 9

    if args.generate:
        num_given_cells = difficulty_to_num_given_cells(N, args.difficulty)
        grid = generate_puzzle(N, num_given_cells)
        print("Generated puzzle:")
        print_grid(grid)

    elif args.solve:
        filename = args.solve
        grid = read_grid_from_file(filename)
        sudoku = Sudoku(grid)
        if sudoku.solve():
            print("Solution:")
            print_grid(sudoku.grid)
        else:
            print("No solution found.")

if __name__ == '__main__':
    main()
