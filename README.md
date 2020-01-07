# Sudoku Solver

In the game of Sudoku, you are given a partially-filled 9×9 grid, grouped into a 3×3 grid of 3×3 blocks. The objective is to fill each square with a digit from 1 to 9, subject to the requirement that each row, column, and block must contain each digit exactly once.

This repository was an exercide to implement the AC-3 constraint satisfaction algorithm from scrath to solve a Sudoku puzzle, along with two extensions that will combine to form a complete and efficient solver.

This was made as an exercise to learn and solve Constraint satisfaction problems (CSP) by using a sudoku puzzle. So please take in account that this code was written in a few days without any professional review/standard.

## Getting Started

The file ["sudoku.py"](sudoku.py) contains all the code to load and solve a sudoku using 3 different techniques:

- AC3 for simple puzzles
- AC3 improved (calls AC3 in subroutines to examine the possible value of other cells in the same row, column, or block) for medium-difficulty puzzles.
- AC3 with quessing for hard puzzles

There are a bunch of txt files as well with sudokus already defined to test the code.

### Prerequisites

- [Numpy](https://numpy.org/)

## Running the solver

Here is how you can make a board from a txt file:

```[python]
sudoku = Sudoku(read_board("easy.txt"))
```

### AC3

```[python]
sudoku = Sudoku(read_board("easy.txt")
sudoku.infer_ac3()
print(sudoku.is_solved)
```

### AC3 improved

```[python]
sudoku = Sudoku(read_board("medium1.txt")
sudoku.infer_improved()
print(sudoku.is_solved)
```

### AC3 with guessing

```[python]
sudoku = Sudoku(read_board("hard1.txt")
sudoku.infer_with_guessing()
print(sudoku.is_solved)
```

## Authors

- **Raphael Van Hoffelen** - [github](https://github.com/dskart) - [website](https://www.raphaelvanhoffelen.com/)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
