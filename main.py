import pygame
import numpy as np

#DEFINE COLORS
WHITE = (255, 255, 255)
GRAY = (211, 211, 211)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (124,252,0)

#DEFINE CONSTANTS
ROW_COUNT = 8
COL_COUNT = 8

SPACES = 3

#INIT BOARD
board = [
['0', '1', '0', '1', '0', '1', '0', '1', '-'], 
['1', '0', '1', '0', '1', '0', '1', '0', '-'],
['0', '1', '0', '1', '0', '1', '0', '1', '-'],
['0', '0', '0', '0', '0', '0', '0', '0', '-'],
['0', '0', '0', '0', '0', '0', '0', '0', '-'],
['2', '0', '2', '0', '2', '0', '2', '0', '-'],
['0', '2', '0', '2', '0', '2', '0', '2', '-'],
['2', '0', '2', '0', '2', '0', '2', '0', '-'],
['-', '-', '-', '-', '-', '-', '-', '-', '-']
]

#PIECES AND TURNS
blank = '0'
black = '1'
red = '2'
bking = '3'
rking = '4'

turn = 0

#DEFINE FUNCTIONS

#DRAW BOARD
def draw_board(): 
    for r in range(ROW_COUNT):
        for c in range(COL_COUNT):
            #DRAW TILES
            if (r + c) % 2 == 0:
                pygame.draw.rect(screen, GRAY, (c * SQUARESIZE, r * SQUARESIZE, SQUARESIZE, SQUARESIZE))
            else:
                pygame.draw.rect(screen, WHITE, (c * SQUARESIZE, r * SQUARESIZE, SQUARESIZE, SQUARESIZE))

            #DRAW PIECES
            if board[r][c] == red:
                pygame.draw.circle(screen, RED, (int(c * SQUARESIZE + SQUARESIZE / 2), int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
            elif board[r][c] == black:
                pygame.draw.circle(screen, BLACK, (int(c * SQUARESIZE + SQUARESIZE / 2), int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
            elif board[r][c] == rking:
                pygame.draw.circle(screen, RED, (int(c * SQUARESIZE + SQUARESIZE / 2), int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
                screen.blit(kingImg, (int(c * SQUARESIZE + SQUARESIZE / 4), int(r * SQUARESIZE + SQUARESIZE / 4)))
            elif board[r][c] == bking:
                pygame.draw.circle(screen, BLACK, (int(c * SQUARESIZE + SQUARESIZE / 2), int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
                screen.blit(kingImg, (int(c * SQUARESIZE + SQUARESIZE / 4), int(r * SQUARESIZE + SQUARESIZE / 4)))
    
    #FILL BOARD    
    pygame.display.update()

#GET ROW AND COLUMN OF CLICK
def get_coords(mouse_pos):
    col = int(mouse_pos[0] / SQUARESIZE)
    row = int((mouse_pos[1]) / SQUARESIZE)
    return row, col

#IS CLICK POSITION VALID?
def valid_click_pos(r, c):
    if turn == 0:
        return board[r][c] == red or board[r][c] == rking
    else:
        return board[r][c] == black or board[r][c] == bking

#IF SO, GET POSSIBLE MOVES
def get_valid_moves(r, c):
    moves = []
    
    #RED PIECE SELECTED
    if turn == 0:
        if (board[r-1][c-1] == blank):
            moves.append([r-1, c-1])
        if (board[r-1][c+1] == blank):
            moves.append([r-1, c+1])
        if ((board[r-1][c-1] == black or board[r-1][c-1] == bking) and board[r-2][c-2] == blank):
            moves.append([r-2, c-2])
        if ((board[r-1][c+1] == black or board[r-1][c+1] == bking) and board[r-2][c+2] == blank):
            moves.append([r-2, c+2])
        #IF RED PIECE IS KING
        if board[r][c] == rking:
            if (board[r+1][c-1] == blank):
                moves.append([r+1, c-1])
            if (board[r+1][c+1] == blank):
                moves.append([r+1, c+1])
            if ((board[r+1][c-1] == black or board[r+1][c-1] == bking) and board[r+2][c-2] == blank):
                moves.append([r+2, c-2])
            if ((board[r+1][c+1] == black or board[r+1][c+1] == bking) and board[r+2][c+2] == blank):
                moves.append([r+2, c+2])
    #BLACK PIECE SELECTED
    else:
        if (board[r+1][c-1] == blank):
            moves.append([r+1, c-1])
        if (board[r+1][c+1] == blank):
            moves.append([r+1, c+1])
        if ((board[r+1][c-1] == red or board[r+1][c-1] == rking) and board[r+2][c-2] == blank):
            moves.append([r+2, c-2])
        if ((board[r+1][c+1] == red or board[r+1][c+1] == rking) and board[r+2][c+2] == blank):
            moves.append([r+2, c+2])
        #IF BLACK PIECE IS KING
        if board[r][c] == bking:
            if (board[r-1][c-1] == blank):
                moves.append([r-1, c-1])
            if (board[r-1][c+1] == blank):
                moves.append([r-1, c+1])
            if ((board[r-1][c-1] == red or board[r-1][c-1] == rking) and board[r-2][c-2] == blank):
                moves.append([r-2, c-2])
            if ((board[r-1][c+1] == red or board[r-1][c+1] == rking) and board[r-2][c+2] == blank):
                moves.append([r-2, c+2])
    return moves

#SHOW POSSIBLE MOVES
def draw_selected(r, c):
    draw_board()
    moves = get_valid_moves(r, c)
    for move in moves:
        pygame.draw.rect(screen, GREEN, (move[1] * SQUARESIZE, move[0] * SQUARESIZE, SQUARESIZE, SQUARESIZE))

#CHECK IF MOVE IS VALID
def is_move_valid(r, c, nr, nc):
    return [nr, nc] in get_valid_moves(r, c) 

#UPDATE BOARD WITH MOVE
def update_board(r, c, nr, nc):
    #MOVES
    if turn == 0:
        if board[r][c] == red:
            board[r][c] = blank
            board[nr][nc] = red
        else:
            board[r][c] = blank
            board[nr][nc] = rking
        #CHECK FOR KING
        if nr == 0:
            board[nr][nc] = rking
    else:
        if board[r][c] == black:
            board[r][c] = blank
            board[nr][nc] = black
        else:
            board[r][c] = blank
            board[nr][nc] = bking
        #CHECK FOR KING
        if nr == ROW_COUNT - 1:
            board[nr][nc] = bking
    #JUMPS
    if (nr==r-2 and nc==c+2):
        board[r-1][c+1] = blank
    if (nr==r-2 and nc==c-2):
        board[r-1][c-1] = blank
    if (nr==r+2 and nc==c+2):
        board[r+1][c+1] = blank
    if (nr==r+2 and nc==c-2):
        board[r+1][c-1] = blank
    
    draw_board()






#DEFINE GRAPHICS
pygame.init()

SMALLSIZE = 50
SQUARESIZE = 75
RADIUS = 30

width = COL_COUNT * SQUARESIZE
height = ROW_COUNT * SQUARESIZE

screen = pygame.display.set_mode([width, height])
pygame.display.flip()

kingImg = pygame.image.load('king.png')
kingImg = pygame.transform.scale(kingImg, (int(SQUARESIZE/2), int(SQUARESIZE/2)))

draw_board()
pygame.display.update()

gameover = False
selected = False
clicked = False
r=0
c=0

while not gameover:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameover = True
       
    if event.type == pygame.MOUSEBUTTONDOWN:
        if not selected:
            r, c = get_coords(event.pos)
            #SHOW PIECE IS SELECTED
            if (valid_click_pos(r, c)):
                selected = True
                draw_selected(r, c)
        else:
            nr, nc = get_coords(event.pos)
            #PLAYER CLICKS ON ANOTHER RED PIECE
            if turn==0 and (board[nr][nc] == red or board[nr][nc] == rking):              
                r=nr
                c=nc
                draw_selected(r, c)
            #PLAYER CLICKS ON ANOTHER BLACK PIECE
            elif turn==1 and (board[nr][nc] == black or board[nr][nc] == bking):
                r=nr
                c=nc
                draw_selected(r, c)
            #PLAYER MOVES HIS PIECE
            elif is_move_valid(r, c, nr, nc):
                update_board(r, c, nr, nc)
                turn +=1
                turn %= 2
                selected = False
                    

    pygame.display.update()

pygame.quit()
quit()