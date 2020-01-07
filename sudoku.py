import random
import queue
import copy
import numpy as np


def sudoku_cells():
    cells = []
    for row in range(9):
        for col in range(9):
            cells.append((row, col))

    return cells


def sudoku_boxes():
    boxes = []

    for bow_row in range(0, 9, 3):
        for bow_col in range(0, 9, 3):
            box = []
            for row in range(bow_row, bow_row+3):
                for col in range(bow_col, bow_col+3):
                    box.append((row, col))
            boxes.append(box)

    return boxes


def sudoku_arcs():
    cells = sudoku_cells()
    boxes = sudoku_boxes()
    arcs = []
    row_col_nums = {0, 1, 2, 3, 4, 5, 6, 7, 8}

    for cell in cells:
        row_arcs = row_col_nums - {cell[0]}
        col_arcs = row_col_nums - {cell[1]}

        for row_arc in row_arcs:
            cell_neighbour = (row_arc, cell[1])
            arcs.append((cell, cell_neighbour))

        for col_arc in col_arcs:
            cell_neighbour = (cell[0], col_arc)
            arcs.append((cell, cell_neighbour))

        for box in boxes:
            if cell in box:
                for box_cell in box:
                    if box_cell != cell:
                        box_arc = (cell, box_cell)
                        if box_arc not in arcs:
                            arcs.append((cell, box_cell))
    return arcs


def read_board(path):
    text_file = open(path)
    text = text_file.read()

    possible_num = {1, 2, 3, 4, 5, 6, 7, 8, 9}
    board = {}
    column_ind = 0
    row_ind = 0
    for char in text:
        if char == '\n':
            row_ind += 1
            column_ind = 0
        else:
            cell = (row_ind, column_ind)
            if char == "*":
                board[cell] = possible_num.copy()
            else:
                board[cell] = {int(char)}
            column_ind += 1

    return board


class Sudoku(object):

    CELLS = sudoku_cells()
    ARCS = sudoku_arcs()
    BOXES = sudoku_boxes()

    def __init__(self, board, depth=0):
        self._board = board
        self.depth = depth

    def get_values(self, cell):
        return self._board[cell]

    def is_solved(self):
        for value in self._board.values():
            if len(value) != 1:
                return False
        return True

    def is_valid(self):
        if not self.is_solved():
            return False

        for arc in self.ARCS:
            cell1 = arc[0]
            cell2 = arc[1]
            if self._board[cell1] == self._board[cell2]:
                return False

        return True

    def remove_inconsistent_values(self, cell1, cell2):
        if len(self.get_values(cell2)) != 1:
            return False

        if len(self._board[cell1]) == 1:
            return False

        self._board[cell1] -= (self._board[cell2])

        return True

    def infer_ac3(self):
        arc_queue = queue.Queue()
        for arc in self.ARCS:
            arc_queue.put(arc)

        while not arc_queue.empty():
            current_arc = arc_queue.get()
            cell1 = current_arc[0]
            cell2 = current_arc[1]
            if self.remove_inconsistent_values(cell1, cell2):
                for arc_neighbour in self.arc_neighbours(cell1, cell2):
                    arc_queue.put((arc_neighbour, cell1))

        if not self.is_valid():
            return 0

        return 1

    def arc_neighbours(self, cell1, cell2):
        for arc in self.ARCS:
            if arc[0] == cell1 and arc[1] != cell2:
                yield arc[1]

    def infer_improved(self):
        while not self.is_solved():
            self.infer_ac3()

            deduct_at_least_one_cell = False
            for cell, values in self.unsolved_cells():
                if self.deduct_value_from_neighbours(
                        cell, values):
                    deduct_at_least_one_cell = True

            if not deduct_at_least_one_cell:
                break

        if not self.is_valid():
            return 0

        return 1

    def unsolved_cells(self):
        for key, value in self._board.items():
            if len(value) != 1:
                yield key, value

    def deduct_value_from_neighbours(self, cell, values):
        deduct_worked = False
        find_neighbours_types = [self.find_row_neighbours,
                                 self.find_col_neighbours, self.find_box_neighbours]
        for find_neighbours in find_neighbours_types:
            possible_neighbour_values = self.deduct_possible_values_of_neighbours(
                cell, find_neighbours)
            possible_value = values - possible_neighbour_values

            if len(possible_value) == 1:
                deduct_worked = True
                self._board[cell] = possible_value

        return deduct_worked

    def deduct_possible_values_of_neighbours(self, cell, find_neighbours):
        possible_neighbour_values = set()
        for neighbour_cell in find_neighbours(cell):
            for value in self._board[neighbour_cell]:
                possible_neighbour_values.add(value)

        return possible_neighbour_values

    def find_row_neighbours(self, cell):
        row_nums = {0, 1, 2, 3, 4, 5, 6, 7, 8}
        neighbour_rows = row_nums - {cell[0]}

        for neighbour_row in neighbour_rows:
            neighbour_cell = (neighbour_row, cell[1])
            yield neighbour_cell

    def find_col_neighbours(self, cell):
        col_nums = {0, 1, 2, 3, 4, 5, 6, 7, 8}
        neighbour_cols = col_nums - {cell[1]}

        for neighbour_col in neighbour_cols:
            neighbour_cell = (cell[0], neighbour_col)
            yield neighbour_cell

    def find_box_neighbours(self, cell):
        for box in self.BOXES:
            if cell in box:
                for neighbour_cell in box:
                    if neighbour_cell != cell:
                        yield neighbour_cell

    def infer_with_guessing(self):
        self.infer_improved()
        if not self.is_solved():
            for cell, values in self.unsolved_cells():
                new_sudoku = Sudoku(copy.deepcopy(self._board), self.depth+1)
                value = values.pop()
                new_sudoku._board[cell] = {value}

                if new_sudoku.infer_with_guessing():
                    self._board = new_sudoku._board.copy()
                    return 1

        if not self.is_valid():
            return 0

        return 1
