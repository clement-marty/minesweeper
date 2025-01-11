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
    :param Assets.Textures textures: The textures to use
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



def render_entire_grid(screen: pygame.Surface, grid: np.ndarray, neighbours_grid: np.ndarray, cell_size: int, textures: Assets.Textures) -> None:
    '''Renders the entire grid on the screen
    
    :param pygame.Surface screen: The screen to render the grid on
    :param np.ndarray grid: The grid to render
    :param np.ndarray neighbours_grid: The grid of neighbouring mines
    :param int cell_size: The size of each cell
    :param Assets.Textures textures: The textures to use
    '''
    for x in range(grid.shape[0]):
        for y in range(grid.shape[1]):
            
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


def render_end_text(screen: pygame.Surface, win: bool, font: pygame.font.Font) -> None:
    '''Displays the end of the game message
    
    :param bool win: Whether the player won or lost
    '''
    rect = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
    text = font.render(
        'You won!' if win else 'You lost!',
        1,
        '#00a000' if win else '#a00000',
    )

    s_w, s_h = screen.get_size()
    t_w, t_h = text.get_size()
    pygame.draw.rect(rect, '#ffffffa0', (
        (s_w - t_w) // 2 - 10,
        (s_h - t_h) // 2 - 10,
        t_w + 20,
        t_h + 20
    ), border_radius=10)
    screen.blit(rect, (0, 0))
    screen.blit(text, (
        (s_w - t_w) // 2,
        (s_h - t_h) // 2
    ))



class Animation:

    def __init__(self, duration: float, delay: float = .0) -> None:
        self.duration = duration
        self.t = -delay

    def is_done(self) -> bool:
        return self.t >= self.duration
    
    def update(self, dt: float):
        raise NotImplementedError('The update method must be implemented in a subclass')
    


class ExplosionAnimation(Animation):

    def __init__(self, textures: list[pygame.Surface], position: tuple[int, int], duration: float, delay: float = .0) -> None:
        '''Initializes the explosion animation
        
        :param list[pygame.Surface] textures: The textures of the animation
        :param tuple[int, int] position: The position of the animation
        :param float duration: The duration of the animation
        :param float delay: The delay before the animation starts
        '''
        super().__init__(duration, delay)
        self.textures = textures

    def update(self, dt: float) -> tuple[pygame.Surface, tuple[int, int]]:
        '''Updates the animation
        
        :param float dt: The time passed since the last frame
        :return tuple[pygame.Surface, tuple[int, int]]: The texture to render and the position of its center
        '''
        self.t += dt
        i = int(self.t / self.duration * len(self.textures))
        return self.textures[min(i, len(self.textures)-1)], (0, 0)