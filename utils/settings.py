import pygame

pygame.init()
pygame.font.init()

WHITE = (255, 255, 255)
BLACK = (0,   0,   0)
RED   = (255, 0,   0)
BLUE  = (0,   255, 0)
GREEN = (0,   0,   255)

FPS = 60

# Definition of grid size
WIDTH, HEIGHT = 600, 700

# Definition of the amount of rows and columns
ROWS = COLS = 50

# Verify grid size
assert ROWS == COLS, "Number of rows and columns must be the same"

# Definition of the minimum toolbar size
MINIMUM_TOOLBAR_SIZE = 100

# Verify toolbar size
assert HEIGHT >= (WIDTH + MINIMUM_TOOLBAR_SIZE), "Height must be greater than width by 100!"

# Definition of the toolbar size (as grid must be squared, the remaining space is toolbar)
TOOLBAR_HEIGHT = HEIGHT - WIDTH

# Calculate the pixel size in actual pixels
PIXEL_SIZE = WIDTH // COLS 

# Macro for the default background color
BG_COLOR = WHITE

DRAW_GRID_LINES = True

# Left click number definition for pygame
LEFT_CLICK = 0


def get_font(size):
    return pygame.font.SysFont("comicsans", size)