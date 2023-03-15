#!/usr/bin/env python3
import sys
import argparse
import random
from math import sqrt
import multiprocessing

class Sudoku:
    def __init__(self, grid, N):
        self.grid = grid
        self.N = N
        self.box_size = int(sqrt(N))

    def is_safe(self, row, col, num):
        return self.is_row_safe(row, num) and self.is_col_safe(col, num) and self.is_box_safe(row, col, num)

    def is_row_safe(self, row, num):
        return num not in self.grid[row]

    def is_col_safe(self, col, num):
        return all(num != self.grid[row][col] for row in range(self.N))

    def is_box_safe(self, row, col, num):
        start_row, start_col = row - row % self.box_size, col - col % self.box_size
        return all(num != self.grid[i + start_row][j + start_col] for i in range(self.box_size) for j in range(self.box_size))

    def find_empty_location(self, start_row, end_row):
        for row in range(start_row, end_row):
            for col in range(self.N):
                if self.grid[row][col] == 0:
                    return row, col
        return None

    def solve(self, start_row=0, end_row=None):
        if end_row is None:
            end_row = self.N

        row_col = self.find_empty_location(start_row, end_row)
        if not row_col:
            return True

        row, col = row_col

        for num in range(1, self.N + 1):
            if self.is_safe(row, col, num):
                self.grid[row][col] = num

                if self.solve(start_row, end_row):
                    return True

                self.grid[row][col] = 0

        return False

def print_grid(grid):
    for row in grid:
        print(row)

def generate_puzzle(N, num_given_cells):
    grid = [[0 for _ in range(N)] for _ in range(N)]
    sudoku = Sudoku(grid, N)

    for _ in range(num_given_cells):
        row, col = random.randint(0, N - 1), random.randint(0, N - 1)
        num = random.randint(1, N)

        while not sudoku.is_safe(row, col, num) or sudoku.grid[row][col] != 0:
            row, col = random.randint(0, N - 1), random.randint(0, N - 1)
            num = random.randint(1, N)

        sudoku.grid[row][col] = num

    return sudoku.grid

def solve_partial_grid(sudoku, start_row, end_row, queue):
    partial_sudoku = Sudoku(sudoku.grid.copy(), sudoku.N)
    if partial_sudoku.solve(start_row, end_row):
        queue.put(partial_sudoku.grid)
    else:
        queue.put(None)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-g", "--generate", help="generate a new puzzle", action="store_true")
    parser.add_argument("-s", "--solve", help="solve a puzzle from a file", type=str)
    parser.add_argument("-d", "--difficulty", help="difficulty level (1-12)", type=int, default=5)
    parser.add_argument("-n", "--num_cells", help="number of cells per side", type=int, default=9)

    args = parser.parse_args()

    if args.generate:
        N = args.num_cells
        num_given_cells = args.difficulty *         N
        grid = generate_puzzle(N, num_given_cells)
        print("Generated puzzle:")
        print_grid(grid)

    elif args.solve:
        with open(args.solve, "r") as f:
            grid = [[int(num) for num in line.strip().split()] for line in f]
            N = len(grid)

        sudoku = Sudoku(grid, N)

        num_workers = multiprocessing.cpu_count()
        rows_per_worker = N // num_workers

        if num_workers <= 1 or N <= 9:
            if sudoku.solve():
                print("Solution:")
                print_grid(sudoku.grid)
            else:
                print("No solution found.")
        else:
            jobs = []
            queue = multiprocessing.Queue()

            for i in range(num_workers):
                start_row = i * rows_per_worker
                end_row = start_row + rows_per_worker if i != num_workers - 1 else N
                process = multiprocessing.Process(target=solve_partial_grid, args=(sudoku, start_row, end_row, queue))
                jobs.append(process)
                process.start()

            for job in jobs:
                job.join()

            while not queue.empty():
                partial_grid = queue.get()
                if partial_grid:
                    print("Solution:")
                    print_grid(partial_grid)
                    break
            else:
                print("No solution found.")

if __name__ == "__main__":
    main()
