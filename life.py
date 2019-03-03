#!usr/bin/python3
# (c) Ethan Peacock
# -----------------------------------------------------------------------

# imports
import sys
import os
import time
import numpy as np


# helper functions
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
    alive = u'\u25cf'
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
    """Determins the next generation by deciding which cells live and die in
        the current generation passed in.

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


def resize_screen(rows, cols):
    if cols < 32:
        cols = 32

    if sys.platform.startswith('win'):
        command = "mode con: cols={0} lines={1}".format(cols + cols, rows + 5)
        os.system(command)
    elif sys.platform.startswith('linux') or sys.platform.startswith('darwin'):
        command = "\x1b[8;{rows};{cols}t".format(rows=rows+3, cols=cols+cols)
        sys.stdout.write(command)
    else:
        print("Unable to resize terminal screen.\n\r")


def prompt():
    """Prompts the user to make a selection for grid before starting game.\

    Args:

    Returns:
        The value of their choice is returned either 1 or 2.  return of 1 means
            we should start a random configuration.  Return of 2 means we
            should load our grid with gliders, simple configs,
            spacship, glidergun, and a random section as well.
    """
    print("~~~~ Conway's Game of Life ~~~~\n")
    print(" Please make a selection for initial cells on grid.\n")
    print("1. Only Randoms on grid.")
    print("2. Gliders, Simples, Glider Guns, Spaceship, and Randoms on grid.")
    while True:
        try:
            answer = int(input("\nSelection: "))
        except ValueError:
            print("\nPlease enter in either 1 or 2 only.")
            continue
        if answer not in [1, 2]:
            print(type(answer))
            print("\nPlease enter in either 1 or 2 only.")
        else:
            break
    return answer


prompt()

# tests
if __name__ == "__main_d_":

    # create explicit 10 x 10 grid
    rows = 55
    cols = 55
    # test_grid = np.zeros((rows, cols), int)
    test_grid = np.zeros((rows, cols))
    next_test_grid = np.zeros((rows, cols))

    # add configurations to grid
    glider = np.array([[1, 0, 0],
                       [0, 1, 1],
                       [1, 1, 0]])

    reverse_glider = np.fliplr(glider)

    simple = np.array([[0, 1, 0],
                       [1, 1, 1],
                       [0, 1, 0]])

    spaceship = np.array([[0, 0, 1, 1, 0],
                          [1, 1, 0, 1, 1],
                          [1, 1, 1, 1, 0],
                          [0, 1, 1, 0, 0]])
    glider_gun =\
    [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0],
     [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0],
     [0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
     [0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
     [1,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
     [1,1,0,0,0,0,0,0,0,0,1,0,0,0,1,0,1,1,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0],
     [0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0],
     [0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
     [0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]

    # add glider gun to grid
    test_grid[40:49, 5:41] = glider_gun

    # add regular glider to grid
    test_grid[1:4, 1:4] = glider

    # add simple configuration to grid
    test_grid[23:26, 15:18] = simple

    # add reverse glider to grid
    test_grid[5:8, 51:54] = reverse_glider

    # add spaceship
    test_grid[28:32, 28:33] = spaceship

    # random configuration
    r = np.random.random((10, 20))
    test_grid[20:30, 30:50] = (r > 0.75)


    # adds a pulsar configuration to grid
    # test_grid[2, 4:7] = 1
    # test_grid[4:7, 7] = 1
    # test_grid += test_grid.T
    # test_grid += test_grid[:, ::-1]
    # test_grid += test_grid[::-1, :]

    # add reverse glider to grid
    # test_grid[:3, 47:50] = reverse_glider
    #
    # test_grid[5:8, :3] = glider

    # np.fill_diagonal(test_grid, 1)

    # add gliders to test grid
    # test_grid[:3, :3] = glider
    # test_grid[19:22, :3] = glider
    # test_grid[:3, 15:18] = glider

    # add simple configuration to grid
    # test_grid[16:19, :3] = simple
    # test_grid[row-3:row, row-8:row-5] = simple
    # test_grid[30:33, 30:33] = simple

    resize_screen(rows, cols)
    for i in range(10000):
        clear_screen()
        print(grid_to_string(test_grid))
        get_next_generation(list(test_grid), list(next_test_grid))
        time.sleep(1 / 6.0)
        # print(grid_to_string(next_test_grid))
        test_grid, next_test_grid = next_test_grid, test_grid
