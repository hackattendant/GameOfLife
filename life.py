#!usr/bin/python3
# (c) Ethan Peacock
# -----------------------------------------------------------------------

# imports
import sys
import os
import time
import numpy as np

# configurations
glider = np.array([[1, 0, 0],
                   [0, 1, 1],
                   [1, 1, 0]])


def clear_screen():
    """Attempts to clear the terminal/console/screen of operating system being
            used to run the program.

    Args: None.

    Returns: None.
    """
    if sys.platform.startswith('darwin') or sys.platform.startswith('linux'):
        os.system('clear')
    elif sys.platform.startswith('win'):
        os.system('cls')
    else:
        print("Program unable to clear your screen\n\r")


def grid_to_string(grid):
    """Takes in grid of 1's and 0's and turns them into a printable string.

    Args:
        grid (np.array):  The grid of 1's and 0's that represent the current
            generation of alive and dead cells.

    Returns:
        A single string with '.' representing dead cells and a unicode circle
            representing the alive cells is returned.
    """
    # unicode circle to represent cells that are alive
    alive = u'\u2588'
    grid_string = ""
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            if grid[row, col] == 0:
                grid_string += ". "
            else:
                grid_string += alive + " "
        grid_string += "\n\r"

    return grid_string


def get_live_neighbors(row, col, rows, cols, grid):
    life_sum = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            if not (i == 0 and j == 0):
                life_sum += grid[((row + i) % rows)][((col + j) % cols)]
    return life_sum


def get_next_generation(rows, cols, grid, next_grid):
    for row in range(rows):
        for col in range(cols):
            # Get the number of live cells adjacent to the cell grid[row][col]
            live_neighbors = get_live_neighbors(row, col, rows, cols, grid)
            if live_neighbors < 2 or live_neighbors > 3:
                next_grid[row][col] = 0
            elif live_neighbors == 3 and grid[row][col] == 0:
                next_grid[row][col] = 1
            else:
                next_grid[row][col] = grid[row][col]





if __name__ == "__main__":
    # create explicit 10 x 10 grid
    rows = 15
    cols = 15
    test_grid = np.zeros((rows, cols), int)
    np.fill_diagonal(test_grid, 1)

    # add glider to test grid
    test_grid[:3, :3] = glider
    next_test_grid = np.zeros((rows, cols))

    for i in range(100):
        clear_screen()
        print(grid_to_string(test_grid))
        get_next_generation(rows, cols, list(test_grid), list(next_test_grid))
        time.sleep(0.7)
        # print(grid_to_string(next_test_grid))
        test_grid, next_test_grid = next_test_grid, test_grid
