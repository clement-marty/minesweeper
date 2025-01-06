import pygame
import configparser

import scripts.assets as Assets
import scripts.game_logic as GameLogic
import scripts.renderer as Renderer

import numpy as np



def init_config() -> None:
    '''Reads the config.ini file'''
    config = configparser.ConfigParser()
    config.read('config.ini')

    global GRID_WIDTH, GRID_HEIGHT, CELL_SIZE, GAME_FPS, MINE_COUNT
    GRID_WIDTH      = config.getint('grid', 'width')
    GRID_HEIGHT     = config.getint('grid', 'height')
    CELL_SIZE       = config.getint('renderer', 'cell_size')
    GAME_FPS        = config.getint('renderer', 'frames_per_second')
    MINE_COUNT      = config.getint('game', 'mine_count')




def game_loop() -> None:
    '''Main game loop'''
    init_config()
    pygame.init()
    pygame.font.init()

    screen = pygame.display.set_mode((
        GRID_WIDTH * CELL_SIZE,
        GRID_HEIGHT * CELL_SIZE
    ))
    pygame.display.set_caption('minesweeper')

    grid = GameLogic.create_grid((GRID_WIDTH, GRID_HEIGHT), MINE_COUNT)
    neighbours_grid = GameLogic.create_neighbours_grid(grid)
    discovered_grid = GameLogic.create_discovered_grid(grid)
    number_font = pygame.font.SysFont('Arial', CELL_SIZE, bold=True)
    text_font = pygame.font.SysFont('Arial', CELL_SIZE*GRID_WIDTH//10, bold=True)
    textures = Assets.Textures(CELL_SIZE, number_font)


    clock = pygame.time.Clock()

    running = True
    has_won = False
    has_lost = False
    while running:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:

                if not has_won and not has_lost: # Check that the game is still running

                    x, y = pygame.mouse.get_pos()
                    x, y = x // CELL_SIZE, y // CELL_SIZE

                    if event.button == 1: # The left mouse button
                        if GameLogic.discover_cell(grid, neighbours_grid, discovered_grid, x, y):
                            has_lost = True

                    elif event.button == 3: # The right mouse button
                        GameLogic.flag_cell(discovered_grid, x, y)
            

        Renderer.render_grid(screen, grid, neighbours_grid, discovered_grid, CELL_SIZE, textures)

        # Check for a win
        if GameLogic.check_win(grid, discovered_grid, MINE_COUNT):
            has_won = True

        # If the game has ended
        if has_won or has_lost:
            Renderer.render_end_text(screen, has_won, text_font)
        
        pygame.display.flip()
        clock.tick(GAME_FPS)

    pygame.quit()



if __name__ == '__main__':
    game_loop()