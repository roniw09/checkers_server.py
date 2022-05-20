import pygame

"""
screen & measures:
"""
WIDTH, HEIGHT = 800, 800
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH // COLS
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))

"""
images used in the game:
"""
OPEN_PIC = 'assets\Checkers entry.png'
CROWN = pygame.transform.scale(pygame.image.load('assets/crown.png'), (44, 25))

"""
colors used in the game:
"""
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREY = (128, 128, 128)
CREAM = (237, 219, 183)
TRANSPARENT = (0, 0, 0, 0)
