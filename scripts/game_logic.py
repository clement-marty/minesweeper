import random
import numpy as np



def create_grid(grid_size: tuple[int, int], mine_count: int) -> np.ndarray:
    '''Creates a grid with bombs
    
    :param tuple[int, int] grid_size: The size of the grid, using format (width, height)
    :param int mine_count: The number of mines to place in the grid
    :return np.ndarray: A 2D list representing the grid, in which:
        - 0 represents an empty cell
        - 1 represents a cell with a mine
    '''
    grid = np.zeros(grid_size, dtype=int)
    
    i = 0
    while i < mine_count:
        x = random.randint(0, grid_size[0] - 1)
        y = random.randint(0, grid_size[1] - 1)
        
        if grid[x, y] == 0:
            grid[x, y] = 1
            i += 1
    
    return grid


def count_neighbours(grid: np.ndarray, x: int, y: int) -> int:
    '''Counts the number of mines in the neighbouring cells
    
    :param np.ndarray grid: The grid to check
    :param int x: The x-coordinate of the cell
    :param int y: The y-coordinate of the cell
    :return int: The number of mines in the neighbouring cells
    '''
    count = 0
    
    for i in range(-1, 2):
        for j in range(-1, 2):
            if not (i == 0 and j == 0) \
                and x+i >= 0 and x+i < grid.shape[0] \
                and y+j >= 0 and y+j < grid.shape[1]:

                count += grid[x+i, y+j]
    
    return count


def create_neighbours_grid(grid: np.ndarray) -> np.ndarray:
    '''Creates a grid in which each cell represents the number of mines in the neighbouring cells
    
    :param np.ndarray grid: The grid to check
    :return np.ndarray: A 2D list representing the grid, in which each cell contains the number of mines in the neighbouring cells
        - cells with mines have a value of -1
    '''
    neighbours_grid = np.zeros(grid.shape, dtype=int)
    for x in range(grid.shape[0]):
        for y in range(grid.shape[1]):
            if grid[x, y] == 0:
                neighbours_grid[x, y] = count_neighbours(grid, x, y)
            else:
                neighbours_grid[x, y] = -1
    return neighbours_grid


def create_discovered_grid(grid: np.ndarray) -> np.ndarray:
    '''Creates a grid in which each cell represents whether it has been discovered
    
    :param np.ndarray grid: The grid of the game
    :return np.ndarray: A 2D list representing the grid, in which:
        - 0 represents an undiscovered cell
        - 1 represents an undiscovered flagged cell
        - 2 represents a discovered cell
    '''
    return np.zeros(grid.shape, dtype=int)



def flag_cell(discovered_grid: np.ndarray, x: int, y: int) -> None:
    '''Flags a cell (or unflags it if it is already flagged)
    
    :param np.ndarray discovered_grid: The grid of discovered cells
    :param int x: The x-coordinate of the cell
    :param int y: The y-coordinate of the cell
    '''
    if discovered_grid[x, y] == 0:
        discovered_grid[x, y] = 1
    elif discovered_grid[x, y] == 1:
        discovered_grid[x, y] = 0


def discover_cell(grid: np.ndarray, neighbours_grid: np.ndarray, discovered_grid: np.ndarray, x: int, y: int) -> tuple[bool, int]:
    '''Discovers a cell and returns if the discovered cell is a mine
    If the chosen cell has no neighbouring mines, the function will discover all the neighbouring cells
    
    :param np.ndarray grid: The grid of the game
    :param np.ndarray discovered_grid: The grid of discovered cells
    :param int x: The x-coordinate of the cell
    :param int y: The y-coordinate of the cell
    :return tuple[bool, int]: A tuple containing:
        - a boolean whose value is True if the discovered cell is a mine, False otherwise
        - an integer representing the number of mines that were discovered
    '''
    stack = [(x, y)]
    discovered_cells = set()
    while stack:
        cx, cy = stack.pop()
        if discovered_grid[cx, cy] != 2:
            discovered_grid[cx, cy] = 2
            discovered_cells.add((cx, cy))
            
            if neighbours_grid[cx, cy] == 0:
                for i in range(-1, 2):
                    for j in range(-1, 2):
                        if not (i == 0 and j == 0) \
                            and cx+i >= 0 and cx+i < grid.shape[0] \
                            and cy+j >= 0 and cy+j < grid.shape[1]:

                            if (cx+i, cy+j) not in discovered_cells:
                                stack.append((cx+i, cy+j))
    
    return grid[x, y] == 1, len(discovered_cells)


def check_win(grid: np.ndarray, discovered_grid: np.ndarray, mine_count: int) -> bool:
    '''Checks if the game has been won, either by flagging all the mines or discovering all the cells
    
    :param np.ndarray grid: The grid of the game
    :param np.ndarray discovered_grid: The grid of discovered cells
    :param int mine_count: The number of mines in the grid
    :return bool: True if the game has been won, False otherwise
    '''
    flagged_bombs = 0
    discovered_cells = 0

    for x in range(grid.shape[0]):
        for y in range(grid.shape[1]):

            if grid[x, y] == 1 and discovered_grid[x, y] == 1:
                flagged_bombs += 1
            
            elif grid[x, y] == 0 and discovered_grid[x, y] == 2:
                discovered_cells += 1

    return flagged_bombs == mine_count or discovered_cells == grid.shape[0] * grid.shape[1] - mine_count
        


def create_from_coords(x: int, y: int, grid_size: tuple[int, int], mine_count: int) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    '''Creates a grid from the position of a cell
    Making sure that the designed cell does not contain a mine

    :param int x: The x-coordinate of the cell
    :param int y: The y-coordinate of the cell
    :param tuple[int, int] grid_size: The size of the grid, using format (width, height)
    :param int mine_count: The number of mines to place in the grid
    :return tuple[np.ndarray, np.ndarray, np.ndarray]: A tuple containing:
        - the grid of the game
        - the grid of neighbours
        - the grid of discovered cells
    '''
    b, n = False, 0
    while b or n <= 1:
        grid = create_grid(grid_size, mine_count)
        neighbours_grid = create_neighbours_grid(grid)
        discovered_grid = create_discovered_grid(grid)
        b, n = discover_cell(grid, neighbours_grid, discovered_grid, x, y)
    return grid, neighbours_grid, discovered_grid