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
    alive = u'\u25ce'
    grid_string = ""
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            if grid[row, col] == 0:
                grid_string += ". "
            else:
                grid_string += alive + " "
        grid_string += "\n\r"

    return grid_string


def get_live_neighbors(row, col, grid):
    """Gets the number of current live cells that are padding around the center
        cell at the element of [row, col] passed in.

    Args:
        row (int): The row of the center cell with padding of cells we want to
            check.
        col (int): The column of the center cell with padding of cells we want
            to check.
        grid (np.array): The grid of 1's and 0's that represent alive and dead
            cells.

    Returns:
        The life_sum number that is the number of alive cells surrounding the
            cell that we are checking.
    """
    rows = len(grid)
    cols = len(grid[0])
    life_sum = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            if not (i == 0 and j == 0):
                life_sum += grid[((row + i) % rows)][((col + j) % cols)]

    return life_sum


def get_next_generation(grid, next_grid):
    """Determins the next generation by deciding which cells live and die in the
        current generation passed in.

    Args:
        grid (np.array): The grid that represents the current alive and dead
            cells.
        next_grid (np.array): The grid that represents the next generation.

    Returns:
        None
    """
    rows = len(grid)
    cols = len(grid[0])
    for row in range(rows):
        for col in range(cols):
            live_neighbors = get_live_neighbors(row, col, grid)
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
    # np.fill_diagonal(test_grid, 1)

    # add glider to test grid
    test_grid[:3, :3] = glider
    next_test_grid = np.zeros((rows, cols))

    for i in range(100):
        clear_screen()
        print(grid_to_string(test_grid))
        get_next_generation(list(test_grid), list(next_test_grid))
        time.sleep(0.3)
        # print(grid_to_string(next_test_grid))
        test_grid, next_test_grid = next_test_grid, test_grid
