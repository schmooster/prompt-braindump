#!/usr/bin/env python3
import sys
import argparse
import random
from typing import List, Tuple


class Sudoku:
    def __init__(self, grid: List[List[int]]):
        self.grid = grid

    def solve(self) -> bool:
        empty_cell = self.find_empty_cell()
        if not empty_cell:
            return True

        row, col = empty_cell
        for num in range(1, len(self.grid) + 1):
            if self.is_safe(row, col, num):
                self.grid[row][col] = num
                if self.solve():
                    return True
                self.grid[row][col] = 0
        return False

    def find_empty_cell(self) -> Tuple[int, int] or None:
        for i in range(len(self.grid)):
            for j in range(len(self.grid)):
                if self.grid[i][j] == 0:
                    return i, j
        return None

    def is_safe(self, row: int, col: int, num: int) -> bool:
        return (
            self.is_row_safe(row, num)
            and self.is_col_safe(col, num)
            and self.is_box_safe(row, col, num)
        )

    def is_row_safe(self, row: int, num: int) -> bool:
        return num not in self.grid[row]

    def is_col_safe(self, col: int, num: int) -> bool:
        return num not in [row[col] for row in self.grid]

    def is_box_safe(self, row: int, col: int, num: int) -> bool:
        start_row = row - row % 3
        start_col = col - col % 3
        for i in range(3):
            for j in range(3):
                if self.grid[i + start_row][j + start_col] == num:
                    return False
        return True


def generate_puzzle(N: int, num_given_cells: int) -> List[List[int]]:
    grid = [[0] * N for _ in range(N)]

    sudoku = Sudoku(grid)
    for _ in range(num_given_cells):
        row = random.randint(0, N - 1)
        col = random.randint(0, N - 1)
        num = random.randint(1, N)

        while not sudoku.is_safe(row, col, num) or sudoku.grid[row][col] != 0:
            row = random.randint(0, N - 1)
            col = random.randint(0, N - 1)
            num = random.randint(1, N)

        sudoku.grid[row][col] = num

    return sudoku.grid


def main():
    parser = argparse.ArgumentParser(description="Generate and solve Sudoku puzzles.")
    parser.add_argument("-g", "--generate", action="store_true", help="Generate a puzzle")
    parser.add_argument("-s", "--solve", metavar="FILE", help="Solve a puzzle from a file")
    parser.add_argument(
        "-d", "--difficulty", type=int, default=1, help="Difficulty level (1-12)"
    )
    parser.add_argument(
        "-n", "--num_cells", type=int, default=9, help="Number of cells per side"
    )

    args = parser.parse_args()

    if args.generate:
        N = args.num_cells
        difficulty = args.difficulty
        num_given_cells = (N ** 2) // (1 + difficulty)
        grid = generate_puzzle(N, num_given_cells)

        print("Generated puzzle:")
        for row in grid:
            print(','.join(map(str, row)))

    elif args.solve:
        input_file = args.solve
        try:
            with open(input_file, "r") as f:
                grid = [list(map(int, line.strip().split(','))) for line in f.readlines()]

            sudoku = Sudoku(grid)
            if sudoku.solve():
                print("Solution:")
                for row in sudoku.grid:
                    print(row)
            else:
                print("No solution exists.")
        except FileNotFoundError:
            print(f"Error: File '{input_file}' not found.")
        except ValueError:
            print("Error: Invalid file format.")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
