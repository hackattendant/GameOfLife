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
    # empty string to hold strings built from array
    grid_string = ""
    # build string for printing
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
        None, grids passed in are mainpulated.
    """
    # get num of rows and cols
    rows = len(grid)
    cols = len(grid[0])
    # build next generation of cells to show during next iteration of game
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

    Args:
        None.

    Returns:
        None.
    """
    if sys.platform.startswith('darwin') or sys.platform.startswith('linux'):
        os.system('clear')
    elif sys.platform.startswith('win'):
        os.system('cls')
    else:
        print("Program unable to clear your screen\n\r")


def resize_screen(rows, cols):
    """Resize the screen/console/terminal to fit grid size in order for pseudo movie to 'run' well.

    Args:
        rows (int): number of rows in grid.
        cols (int): number of columns in grid.

    Returns:
        None, the terminal/console/window of system is just resized with commands.
    """
    if cols < 30:
        cols = 30
    if sys.platform.startswith('win'):
        command = "mode con: cols={0} lines={1}".format(cols + cols, rows + 5)
        os.system(command)
    elif sys.platform.startswith('linux') or sys.platform.startswith('darwin'):
        command = "\x1b[8;{rows};{cols}t".format(rows=rows+10, cols=cols+cols)
        sys.stdout.write(command)
    else:
        print("Unable to resize terminal screen.\n\r")


def prompt_cells():
    """Prompts the user to make a selection for grid before starting game.

    Args:
        None.

    Returns:
        The value of their choice is returned either 1 or 2.  return of 1 means
            we should start a random configuration.  Return of 2 means we
            should load our grid with gliders, simple configs,
            spaceship, glider gun, and a random section as well.
    """
    print("~~~~~~~~~~~~ Conway's Game of Life ~~~~~~~~~~~~\n")
    print(" Please make a selection for initial cells on grid.\n")
    print("1. Only Randoms on grid.")
    print("2. Glider, Simple, Glider Gun, Spaceship, and Random on grid.")
    while True:
        try:
            answer = int(input("\nSelection: "))
        except ValueError:
            print("\nPlease enter in either 1 or 2 only.")
            continue
        if answer not in [1, 2]:
            print("\nPlease enter in either 1 or 2 only.")
        else:
            break

    return answer


def prompt_iterations():
    """Prompts the user to make a selection for how many iterations to run.

    Args:
        None.
    Returns:
        The number of iterations between 1 and 10,000 is returned for the loop that shows the grid.
    """
    print("\nChoose iterations for game to run (1 - 10,000)")
    while True:
        try:
            answer = int(input("\nIterations: "))
        except ValueError:
            print("\nPlease enter in an int between 1 & 10,000 only.")
            continue
        iter_range = [xi + 1 for xi in range(10000)]
        if answer not in iter_range:
            print(type(answer))
            print("\nPlease enter in an int between 1 & 10,000 only.")
        else:
            break

    return answer


def game():
    """Configures the grid and runs the game.

    Args:
        None.

    Returns:
        None. The game is displayed in the console."""
    # initialize configurations
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

    # clear the screen to print out prompts to User
    clear_screen()
    # set rows and columns for grid size
    rows = 55
    cols = 55
    # initialize grid
    my_grid = np.zeros((rows, cols), int)
    next_grid = np.zeros((rows, cols), int)

    # get configuration selection and iterations for game to run
    cell_configuration = prompt_cells()
    grid_iterations = prompt_iterations()

    # configuration for completely random board (user slection 1)
    if cell_configuration == 1:
        rand_grid = []
        for row in range(rows):
            grid_rows = []
            for col in range(cols):
                # Generate a random number and based on that decide whether to add a live or dead cell to the grid
                if np.random.random_integers(0, 7) == 0:
                    grid_rows += [1]
                else:
                    grid_rows += [0]
            rand_grid += [grid_rows]
        my_grid = np.array(rand_grid)

    # configuration for curated grid with custom configurations
    #   (user selection 2)
    else:
        # add glider gun to grid
        my_grid[40:49, 5:41] = glider_gun
        # add regular glider to grid
        my_grid[1:4, 1:4] = glider
        # add reverse glider to grid
        my_grid[5:8, 51:54] = reverse_glider
        # add simple configuration to grid
        my_grid[23:26, 15:18] = simple
        # add spaceship to grid
        my_grid[28:32, 28:33] = spaceship
        # add small random configuration to grid
        r = np.random.random((10, 20))
        my_grid[20:30, 30:50] = (r > 0.75)

    # Display Game
    # resize window to fit grid
    resize_screen(rows, cols)
    # run game for iterations specified by user
    for i in range(grid_iterations):
        clear_screen()
        print("Iteration {}".format(i + 1))
        print(grid_to_string(my_grid))
        get_next_generation(list(my_grid), list(next_grid))
        time.sleep(1 / 5.0)
        # update grids for next generation of printing
        my_grid, next_grid = next_grid, my_grid


if __name__ == "__main__":
    # Run game and display output
    game()
