import os
import getopt
import random
import sys
import time

class GameOfLife:
    """For playing Conways Game of Life

    Has an added feature which is that of having immortal cells
    """

    # Map of letters so we know how to draw them
    letters = {
        'a': [
            [0, 1, 1, 1, 0],
            [1, 0, 0, 0, 1],
            [1, 0, 0, 0, 1],
            [1, 0, 0, 0, 1],
            [1, 1, 1, 1, 1],
            [1, 0, 0, 0, 1],
            [1, 0, 0, 0, 1],
        ],
        'b': [
            [1, 1, 1, 1, 0],
            [1, 0, 0, 0, 1],
            [1, 0, 0, 0, 1],
            [1, 1, 1, 1, 0],
            [1, 0, 0, 0, 1],
            [1, 0, 0, 0, 1],
            [1, 1, 1, 1, 0],
        ],
        'c': [
            [0, 1, 1, 1, 0],
            [1, 0, 0, 0, 1],
            [1, 0, 0, 0, 0],
            [1, 0, 0, 0, 0],
            [1, 0, 0, 0, 0],
            [1, 0, 0, 0, 1],
            [0, 1, 1, 1, 0],
        ],
        'd': [
            [1, 1, 1, 1, 0],
            [1, 0, 0, 0, 1],
            [1, 0, 0, 0, 1],
            [1, 0, 0, 0, 1],
            [1, 0, 0, 0, 1],
            [1, 0, 0, 0, 1],
            [1, 1, 1, 1, 0],
        ],
        'r': [
            [1, 1, 1, 1, 0],
            [1, 0, 0, 0, 1],
            [1, 0, 0, 0, 1],
            [1, 1, 1, 1, 0],
            [1, 0, 1, 0, 0],
            [1, 0, 0, 1, 0],
            [1, 0, 0, 0, 1],
        ],
    }

    matrix = [[]]
    immortal_cells = [[]]
    width = 0
    height = 0
    half_width = 0
    half_height = 0

    t = 0

    def __init__(self, rows, cols):
        """Initialize with (rows: int), (cols: int)"""

        # Set some useful information

        self.width = cols
        self.height = rows

        # Allocate the matrix
        self.matrix = [[0 for x in range(self.width)] for y in range(self.height)]

        self.half_width = int(cols / 2)
        self.half_height = int(rows / 2)

        self._set_start_config()
        self._set_immortal_cells()

    def _set_start_config(self):
        cells = [
            [1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
            [1, 1, 0, 1, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 1, 1, 0, 0, 0, 0],
            [1, 1, 1, 0, 0, 1, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        ]

        mid_j = (self.half_height - 5)
        mid_i = (self.half_width - 5)

        for j, item_j in enumerate(cells):
            for i, item_i in enumerate(item_j):
                self.matrix[mid_j + j][mid_i + i] = cells[j][i]

    def _set_immortal_cells(self):
        """Sets some cells that once they have come to life, will never die"""
        self.immortal_cells = [[0 for x in range(self.width)] for y in range(self.height)]

        # The text to write
        text = "abcd"

        margin_j = 5
        margin_i = 5

        space = 0
        for l, letter in enumerate(list(text)):
            letter_map = self.letters[letter]
            for j, item_j in enumerate(letter_map):
                for i, item_i in enumerate(item_j):
                    self.immortal_cells[margin_j+j][margin_i+space+i] = letter_map[j][i]
            space += 6

    def play_frame(self):
        """Plays one frame of a game of life"""
        # Operate on this matrix which will replace the existing
        back_matrix = [[0 for x in range(self.width)] for y in range(self.height)]

        for j, item_j in enumerate(self.matrix):
            for i, item_i in enumerate(item_j):
                back_matrix[j][i] = self.get_new_cell_state(j, i)

        # Swaperoo
        self.matrix = back_matrix

    def print_frame(self):
        """prints a frame"""
        frame = ""
        for j, item_j in enumerate(self.matrix):
            for i, item_i in enumerate(item_j):
                frame += "\033[{0};{1}H".format(j+1, i+1)
                if bool(self.matrix[j][i]) and bool(self.immortal_cells[j][i]):
                    frame += "@"
                elif bool(self.matrix[j][i]):
                    frame += "."
                else:
                    frame += " "

        print(frame)

    def get_new_cell_state(self, y, x):
        """Plays the rules on a cell to work out if it should live or die"""
        # Any live cell with fewer than two live neighbours dies, as if caused by under-population.
        # Any live cell with two or three live neighbours lives on to the next generation.
        # Any live cell with more than three live neighbours dies, as if by over-population.
        # Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.
        is_alive = bool(self.matrix[y][x])

        # If it's an immortal cell that has come to life then never die
        if is_alive and bool(self.immortal_cells[y][x]):
            return 1

        # Array of neighbours
        neighbours = self._get_neighbours(
                y, x, self.width, self.height, self.matrix)

        # Number of neighbours who are alive
        alive_neighbours = sum(neighbours)

        ## # Array of immortal neighbours
        ## immortals = self._get_neighbours(
        ##         y, x, self.width, self.height, self.immortal_cells)

        ## # Number of neighbours ∪ importals
        ## num_alive_immortal_neighbours = 0
        ## for cell, cell_item in enumerate(neighbours):
        ##     if neighbours[cell] and immortals[cell]:
        ##         num_alive_immortal_neighbours += 1

        ## # @TODO(mark): is there something we can do here to give definition to
        ## #              the letters?
        ## if num_alive_immortal_neighbours > 3:
        ##     return 0

        if is_alive:
            if alive_neighbours < 2:
                return 0
            elif alive_neighbours < 4:
                return 1
            return 0

        if alive_neighbours == 3:
            return 1

        return 0

    def _get_neighbours(self, y, x, width, height, matrix):
        """returns an array of neighbours, ordered top left to bottom
        right
        """
        neighbours = []
        if y > 0:
            if x > 0:
                neighbours.append(matrix[y-1][x-1]) # top left
            if x < width-1:
                neighbours.append(matrix[y-1][x+1]) # top right
            neighbours.append(matrix[y-1][x]) # above

        if x > 0:
            neighbours.append(matrix[y][x-1]) # left
        if x < width-1:
            neighbours.append(matrix[y][x+1]) # right

        if y < height-1:
            if x > 0:
                neighbours.append(matrix[y+1][x-1]) # bottom left
            if x < width-1:
                neighbours.append(matrix[y+1][x+1]) # bottom right
            neighbours.append(matrix[y+1][x]) # above

        return neighbours

def main():
    rows, cols = _get_canvas_size(sys.argv[1:])
    game_of_life = GameOfLife(rows, cols)

    for t in range(500):
        game_of_life.play_frame()
        game_of_life.print_frame()
        time.sleep(0.01)

def _get_canvas_size(argv):
    """Returns the columns and rows to use, giving us the terminal canvas size

    returns <int, int> in order 'rows', 'columns'
    """

    help_message = 'game_of_life.py -c <columns> -r <rows>'
    error_not_valid = 'specified number is invalid'

    try:
        opts, args = getopt.getopt(argv, "c:r:", ["columns=rows="])
    except getopt.GetoptError:
        print(help_message)
        sys.exit(2)

    # Some reasonable defaults
    rows = 20
    cols = 40

    for opt, arg in opts:
        if opt == '-h':
            print(help_message)
            sys.exit()
        elif opt in ("-r", "--rows"):
            try:
                rows = int(arg)
            except:
                print(error_not_valid)
        elif opt in ("-c", "--columns"):
            try:
                cols = int(arg)
            except:
                print(error_not_valid)

    return rows, cols

if __name__ == "__main__":
    main()

