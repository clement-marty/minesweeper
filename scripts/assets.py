import pygame


class Textures:
    '''A class to store all the textures'''
    hidden_cell_background: pygame.Surface
    cell_background: pygame.Surface
    mine: pygame.Surface
    flag: pygame.Surface
    number_1: pygame.Surface
    number_2: pygame.Surface
    number_3: pygame.Surface
    number_4: pygame.Surface
    number_5: pygame.Surface
    number_6: pygame.Surface
    number_7: pygame.Surface
    number_8: pygame.Surface

    def __init__(self, cell_size: int, number_font: pygame.font.Font) -> None:
        '''Initializes the textures'''

        self.init_hidden_cell_background(cell_size)
        self.init_cell_background(cell_size)
        self.init_mine(cell_size)
        self.init_flag(cell_size)
        self.init_numbers(cell_size, number_font)



    def init_hidden_cell_background(self, cell_size: int) -> None:
        '''Initializes the hidden cell background'''
        self.hidden_cell_background = pygame.Surface((cell_size, cell_size))
        self.hidden_cell_background.fill('#808080')
        rects = [
            (cell_size - cell_size//8, 0, cell_size//8, cell_size),
            (0, cell_size - cell_size//8, cell_size, cell_size//8),
            (0, 0, cell_size//8, cell_size),
            (0, 0, cell_size, cell_size//8)
        ]
        colors = ['#606060', '#606060', '#A0A0A0', '#A0A0A0']
        for r, c in zip(rects, colors):
            pygame.draw.rect(self.hidden_cell_background, c, r)
    
    def init_cell_background(self, cell_size: int) -> None:
        '''Initializes the cell background'''
        self.cell_background = pygame.Surface((cell_size, cell_size))
        self.cell_background.fill('#C0C0C0')

    def init_mine(self, cell_size: int) -> None:
        '''Initializes the mine texture'''
        self.mine = pygame.Surface((cell_size, cell_size), pygame.SRCALPHA)
        pygame.draw.circle(self.mine, '#000000', (cell_size//2, cell_size//2), cell_size//3)

        polygons = [
            (
                (cell_size//2 - cell_size//16, cell_size//8),
                (cell_size//2 + cell_size//16, cell_size//8),
                (cell_size//2 + cell_size//16, cell_size - cell_size//8),
                (cell_size//2 - cell_size//16, cell_size - cell_size//8)
            ),
            (
                (cell_size//8, cell_size//2 - cell_size//16),
                (cell_size - cell_size//8, cell_size//2 - cell_size//16),
                (cell_size - cell_size//8, cell_size//2 + cell_size//16),
                (cell_size//8, cell_size//2 + cell_size//16)
            ),
            (
                (cell_size//6 + cell_size//16, cell_size//6),
                (cell_size//6, cell_size//6 + cell_size//16),
                (cell_size - cell_size//6 - cell_size//16, cell_size - cell_size//6),
                (cell_size - cell_size//6, cell_size - cell_size//6 - cell_size//16)
            ),
            (
                (cell_size//6, cell_size - cell_size//6 - cell_size//16),
                (cell_size//6 + cell_size//16, cell_size - cell_size//6),
                (cell_size - cell_size//6, cell_size//6 + cell_size//16),
                (cell_size - cell_size//6 - cell_size//16, cell_size//6)
            )
        ]
        for p in polygons:
            pygame.draw.polygon(self.mine, '#000000', p)


    def init_flag(self, cell_size: int) -> None:
        '''Initializes the flag texture'''
        self.flag = pygame.Surface((cell_size, cell_size), pygame.SRCALPHA)
        pygame.draw.rect(self.flag, '#ff0000', (
            cell_size//2 - cell_size//16, cell_size//8,
            cell_size//8, cell_size - cell_size//8
        ))
        pygame.draw.polygon(self.flag, '#ff0000',[
            (cell_size//2 + cell_size//16, cell_size//8),
            (cell_size - cell_size//8, 5*cell_size//16),
            (cell_size//2 + cell_size//16, cell_size//2)
        ])

    def init_numbers(self, cell_size: int, font: pygame.font.Font) -> None:
        '''Initializes the number textures'''
        color_gradient = [
            '#084CFB', '#63CA23',
            '#7DA81D', '#978717',
            '#B16512', '#CB430C',
            '#E52206', '#FF0000'
        ]
        for i, c in zip(list(range(1, 9)), color_gradient):
            s = pygame.Surface((cell_size, cell_size), pygame.SRCALPHA)

            text = font.render(str(i), 1, c)
            t_w, t_h = text.get_size()
            s.blit(text,(
                (cell_size - t_w) // 2,
                (cell_size - t_h) // 2
            ))
            self.__dict__[f'number_{i}'] = s



class SoundEffects:

    def __init__(self, sound_volume: float) -> None:
        '''Initializes the sound effects'''
        self.bomb_explodes = pygame.mixer.Sound('sounds/bomb_explodes.wav')
        self.flag_placed = pygame.mixer.Sound('sounds/flag_placed.wav')
        self.cell_discovered = pygame.mixer.Sound('sounds/cell_discovered.wav')

        self.bomb_explodes.set_volume(sound_volume)
        self.flag_placed.set_volume(sound_volume)
        self.cell_discovered.set_volume(sound_volume)


class Music:

    def __init__(self, sound_volume: float) -> None:
        '''Initializes the music'''
        self.music = pygame.mixer.music.load('sounds/background_music.mp3')
        pygame.mixer.music.set_volume(sound_volume)
        pygame.mixer.music.play(-1)