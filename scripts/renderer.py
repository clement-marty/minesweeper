import pygame
import numpy as np

import scripts.assets as Assets


def render_grid(screen: pygame.Surface, grid: np.ndarray, neighbours_grid: np.ndarray, discovered_grid: np.ndarray, cell_size: int, textures: Assets.Textures) -> None:
    '''Renders the grid on the screen
    
    :param pygame.Surface screen: The screen to render the grid on
    :param np.ndarray grid: The grid to render
    :param np.ndarray neighbours_grid: The grid of neighbouring mines
    :param np.ndarray discovered_grid: The grid of rendered cells
    :param int cell_size: The size of each cell
    '''
    for x in range(grid.shape[0]):
        for y in range(grid.shape[1]):
            
            if discovered_grid[x, y] == 2: # If the cell has already been discovered
                
                screen.blit(
                    textures.cell_background,
                    (x*cell_size, y*cell_size)
                )

                neighbours = neighbours_grid[x, y]
                if neighbours > 0: # If the cell has neighbouring mines
                    screen.blit(
                        textures.__dict__[f'number_{neighbours_grid[x, y]}'],
                        (x*cell_size, y*cell_size)
                    )

                if grid[x, y] == 1: # If the cell is a mine
                    screen.blit(
                        textures.mine,
                        (x*cell_size, y*cell_size)
                    )

            else: # If the cell has not been discovered
                screen.blit(textures.hidden_cell_background, (x*cell_size, y*cell_size))

                if discovered_grid[x, y] == 1: # If the cell has been flagged
                    screen.blit(textures.flag, (x*cell_size, y*cell_size))

def render_end_text(screen: pygame.Surface, win: bool, font: pygame.font.Font) -> None:
    '''Displays the end of the game message
    
    :param bool win: Whether the player won or lost
    '''
    text = font.render(
        'You won!' if win else 'You lost!',
        1,
        '#00ff00' if win else '#ff0000'
    )

    s_w, s_h = screen.get_size()
    t_w, t_h = text.get_size()
    screen.blit(text, (
        (s_w - t_w) // 2,
        (s_h - t_h) // 2
    ))
