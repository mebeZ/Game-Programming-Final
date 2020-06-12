import pygame
import numpy as np

#DEFINE COLORS
WHITE = (255, 255, 255)
GRAY = (211, 211, 211)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

#DEFINE CONSTANTS
ROW_COUNT = 8
COL_COUNT = 8

SPACES = 3

#DEFINE FUNCTIONS
def draw_board():
    #DRAW BOARD
    for r in range(ROW_COUNT):
        for c in range(COL_COUNT):
            if (r + c) % 2 == 0:
                pygame.draw.rect(screen, GRAY, (c * SQUARESIZE, r * SQUARESIZE, SQUARESIZE, SQUARESIZE))
                if (r < SPACES):
                    pygame.draw.circle(screen, BLACK, (int(c * SQUARESIZE + SQUARESIZE / 2), int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
                if (r > ROW_COUNT - (SPACES + 1)):
                    pygame.draw.circle(screen, RED, (int(c * SQUARESIZE + SQUARESIZE / 2), int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
            else:
                pygame.draw.rect(screen, WHITE, (c * SQUARESIZE, r * SQUARESIZE, SQUARESIZE, SQUARESIZE))
    
    #FILL BOARD    
    pygame.display.update()

def get_coords(mouse_pos):
    col = int(mouse_pos[0] / SQUARESIZE)
    row = int((height - mouse_pos[1]) / SQUARESIZE)
    return row, col

def valid_click_pos(r, c):
    return r < SPACES and (r + c) % 2 == 1


#DEFINE GRAPHICS
pygame.init()

SQUARESIZE = 75
RADIUS = 30

width = COL_COUNT * SQUARESIZE
height = ROW_COUNT * SQUARESIZE

screen = pygame.display.set_mode([width, height])
pygame.display.flip()

draw_board()
pygame.display.update()

gameover = False
selected = False


while not gameover:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameover = True
       
    if event.type == pygame.MOUSEBUTTONDOWN:
        #IS MOUSE CLICKING ON A PIECE
        row, col = get_coords(event.pos)
        if valid_click_pos(row, col) and not selected:
            pygame.draw.circle(screen, YELLOW, (int(col * SQUARESIZE + SQUARESIZE / 2), height - int(row * SQUARESIZE + SQUARESIZE / 2)), RADIUS + 1, 3)
            selected = True


        

    pygame.display.update()

pygame.quit()
quit()