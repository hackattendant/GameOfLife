#!usr/bin/python3
# (c) Ethan Peacock
# -----------------------------------------------------------------------

# imports
import numpy as np

# configurations
glider = np.array([[1, 0, 0],
                   [0, 1, 1],
                   [1, 1, 0]])

# create explicit 10 x 10 grid
test_grid = np.zeros((10, 10), int)
# np.fill_diagonal(test_grid, 1)

# add glider to test grid
test_grid[:3, :3] = glider


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
    for row in range(10):
        for col in range(10):
            if grid[row, col] == 0:
                grid_string += ". "
            else:
                grid_string += alive + " "
        grid_string += "\n\r"

    return grid_string


if __name__ == "__main__":
    grid_string = grid_to_string(test_grid)
    print(grid_string)
