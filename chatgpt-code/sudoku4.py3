#!/usr/bin/env python3
import sys
import random
import copy
import argparse

class Sudoku:
    def __init__(self, grid=None):
        if grid:
            self.grid = grid
        else:
            self.grid = [[0 for _ in range(9)] for _ in range(9)]

    def is_valid(self, row, col, num):
        for i in range(9):
            if self.grid[row][i] == num or self.grid[i][col] == num:
                return False

        start_row, start_col = row - row % 3, col - col % 3
        for i in range(3):
            for j in range(3):
                if self.grid[i + start_row][j + start_col] == num:
                    return False

        return True

    def solve(self, ensure_unique_solution=False):
        row, col = -1, -1
        empty = True
        for i in range(9):
            for j in range(9):
                if self.grid[i][j] == 0:
                    row, col = i, j
                    empty = False
                    break
            if not empty:
                break

        if empty:
            return self.grid

        for num in range(1, 10):
            if self.is_valid(row, col, num):
                self.grid[row][col] = num
                if ensure_unique_solution and not self.solve(ensure_unique_solution):
                    return None
                if self.solve():
                    return self.grid
                self.grid[row][col] = 0

        return None

def generate_sudoku():
    sudoku = Sudoku()
    solved_grid = sudoku.solve()

    grid = copy.deepcopy(solved_grid)
    for _ in range(30):
        row = random.randint(0, 8)
        col = random.randint(0, 8)
        grid[row][col] = 0

    sudoku.grid = copy.deepcopy(grid)
    if sudoku.solve(ensure_unique_solution=True):
        return grid
    else:
        return generate_sudoku()

def main():
    parser = argparse.ArgumentParser(description="Sudoku generator and solver")
    parser.add_argument("-g", "--generate", action="store_true", help="Generate a Sudoku puzzle")
    parser.add_argument("-s", "--solve", action="store_true", help="Solve a Sudoku puzzle")
    parser.add_argument("-gs", "--generate_and_solve", action="store_true", help="Generate and solve a Sudoku puzzle")
    parser.add_argument("-i", "--input", metavar="INPUT", type=str, help="Input file containing Sudoku grid")
    args = parser.parse_args()

    if args.generate:
        grid = generate_sudoku()
        print("Generated Sudoku puzzle:")
        for row in grid:
            print(row)
    elif args.solve:
        if args.input:
            with open(args.input, "r") as f:
                lines = f.readlines()
                grid = [list(map(int, line.strip().split())) for line in lines]

            sudoku = Sudoku(grid)
            solution = sudoku.solve()

            if solution:
                print("Solved Sudoku puzzle:")
                for row in solution:
                    print(row)
            else:
                print("No solution found for the input Sudoku puzzle.")
        else:
            print("Error: Input file is required when solving a Sudoku puzzle.")
    elif args.generate_and_solve:
        grid = generate_sudoku()
        print("Generated Sudoku puzzle:")
        for row in grid:
            print(row)
        
        sudoku = Sudoku(grid)
        solution = sudoku.solve()

        if solution:
            print("\nSolved Sudoku puzzle:")
            for row in solution:
                print(row)
        else:
            print("\nNo solution found for the generated Sudoku puzzle.")
    else:
        print("Error: Please use --generate, --solve or --generate_and_solve flags to specify the action.")

if __name__ == "__main__":
    main()
