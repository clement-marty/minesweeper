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

        self.hidden_cell_background = pygame.Surface((cell_size, cell_size))
        self.hidden_cell_background.fill('#808080')
        pygame.draw.rect(self.hidden_cell_background, '#606060', (
            cell_size - cell_size//8, 0,
            cell_size//8, cell_size
        ))
        pygame.draw.rect(self.hidden_cell_background, '#606060', (
            0, cell_size - cell_size//8,
            cell_size, cell_size//8
        ))
        pygame.draw.rect(self.hidden_cell_background, '#A0A0A0', (
            0, 0,
            cell_size//8, cell_size
        ))
        pygame.draw.rect(self.hidden_cell_background, '#A0A0A0', (
            0, 0,
            cell_size, cell_size//8
        ))

        self.cell_background = pygame.Surface((cell_size, cell_size))
        self.cell_background.fill('#C0C0C0')

        self.mine = pygame.Surface((cell_size, cell_size), pygame.SRCALPHA)
        pygame.draw.circle(self.mine, '#000000', (cell_size//2, cell_size//2), cell_size//2)

        self.flag = pygame.Surface((cell_size, cell_size), pygame.SRCALPHA)
        pygame.draw.rect(self.flag, '#ff0000', (
            cell_size//2 - cell_size//8, cell_size//8,
            cell_size//4, cell_size - cell_size//4
        ))
        pygame.draw.polygon(self.flag, '#ff0000',[
            (cell_size//2, cell_size//8),
            (cell_size - cell_size//8, cell_size//4),
            (cell_size//2, cell_size//2)
        ])


        color_gradient = [
            '#084CFB', '#63CA23',
            '#7DA81D', '#978717',
            '#B16512', '#CB430C',
            '#E52206', '#FF0000'
        ]
        for i, c in zip(list(range(1, 9)), color_gradient):
            s = pygame.Surface((cell_size, cell_size), pygame.SRCALPHA)

            text = number_font.render(str(i), 1, c)
            t_w, t_h = text.get_size()
            s.blit(text,(
                (cell_size - t_w) // 2,
                (cell_size - t_h) // 2
            ))
            self.__dict__[f'number_{i}'] = s
