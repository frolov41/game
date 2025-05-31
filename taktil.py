import pygame
import sys
import random

pygame.init()

CELL_SIZE = 100
BOARD_SIZE = 4
WIDTH = HEIGHT = CELL_SIZE * BOARD_SIZE
FPS = 30

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
RED = (220, 50, 50)
BLUE = (50, 50, 220)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Так-Тиль')
clock = pygame.time.Clock()

board = [[0 for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

for i in range(BOARD_SIZE):
    if i % 2 == 0:
        board[0][i] = 1
        board[BOARD_SIZE-1][i] = 2
    else:
        board[0][i] = 2
        board[BOARD_SIZE-1][i] = 1

selected = None
turn = 1
mode = None 

font_menu = pygame.font.SysFont(None, 48)
font_button = pygame.font.SysFont(None, 36)

def draw_menu():
    screen.fill(WHITE)
    title = font_menu.render('Выберите режим игры', True, BLACK)
    screen.blit(title, (WIDTH//2 - title.get_width()//2, 60))
    btn1 = pygame.Rect(WIDTH//2-150, 150, 300, 70)
    btn2 = pygame.Rect(WIDTH//2-150, 250, 300, 70)
    pygame.draw.rect(screen, GRAY, btn1)
    pygame.draw.rect(screen, GRAY, btn2)
    text1 = font_button.render('Играть вдвоем', True, BLACK)
    text2 = font_button.render('Играть с ботом', True, BLACK)
    screen.blit(text1, (btn1.x + (btn1.width-text1.get_width())//2, btn1.y + 15))
    screen.blit(text2, (btn2.x + (btn2.width-text2.get_width())//2, btn2.y + 15))
    pygame.display.flip()
    return btn1, btn2

def draw_board():
    screen.fill(WHITE)
    for y in range(BOARD_SIZE):
        for x in range(BOARD_SIZE):
            rect = pygame.Rect(x*CELL_SIZE, y*CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, GRAY, rect, 1)
            if board[y][x] == 1:
                pygame.draw.circle(screen, BLACK, rect.center, CELL_SIZE//2-8)
                pygame.draw.circle(screen, WHITE, rect.center, CELL_SIZE//2-16)
                pygame.draw.circle(screen, BLACK, rect.center, CELL_SIZE//2-8, 3)
            elif board[y][x] == 2:
                pygame.draw.circle(screen, BLACK, rect.center, CELL_SIZE//2-8)
                pygame.draw.circle(screen, BLACK, rect.center, CELL_SIZE//2-16)
                pygame.draw.circle(screen, BLACK, rect.center, CELL_SIZE//2-8, 3)
            if selected == (y, x):
                pygame.draw.rect(screen, (0, 255, 0), rect, 3)

def get_cell(pos):
    x, y = pos
    cx, cy = x // CELL_SIZE, y // CELL_SIZE
    if 0 <= cx < BOARD_SIZE and 0 <= cy < BOARD_SIZE:
        return cy, cx
    return None

def can_move(from_cell, to_cell):
    fy, fx = from_cell
    ty, tx = to_cell
    if board[ty][tx] != 0:
        return False
    if abs(fy-ty) + abs(fx-tx) != 1:
        return False
    return True

def check_win():
    for y in range(BOARD_SIZE):
        for x in range(BOARD_SIZE):
            if board[y][x] == 0:
                continue
            color = board[y][x]
            if x+2 < BOARD_SIZE and all(board[y][x+i] == color for i in range(3)):
                return color
            if y+2 < BOARD_SIZE and all(board[y+i][x] == color for i in range(3)):
                return color
            if x+2 < BOARD_SIZE and y+2 < BOARD_SIZE and all(board[y+i][x+i] == color for i in range(3)):
                return color
            if x-2 >= 0 and y+2 < BOARD_SIZE and all(board[y+i][x-i] == color for i in range(3)):
                return color
    return 0

def bot_move():
    moves = []
    for y in range(BOARD_SIZE):
        for x in range(BOARD_SIZE):
            if board[y][x] == 2:
                for dy, dx in [(-1,0),(1,0),(0,-1),(0,1)]:
                    ny, nx = y+dy, x+dx
                    if 0 <= ny < BOARD_SIZE and 0 <= nx < BOARD_SIZE and board[ny][nx] == 0:
                        moves.append(((y, x), (ny, nx)))
    if moves:
        move = random.choice(moves)
        fy, fx = move[0]
        ty, tx = move[1]
        board[ty][tx] = 2
        board[fy][fx] = 0
        return True
    return False

running = True
winner = 0
menu = True
while running:
    if menu:
        btn1, btn2 = draw_menu()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if btn1.collidepoint(event.pos):
                    mode = 1
                    menu = False
                elif btn2.collidepoint(event.pos):
                    mode = 2
                    menu = False
        continue
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and winner == 0:
            cell = get_cell(event.pos)
            if cell:
                y, x = cell
                if selected:
                    if can_move(selected, cell):
                        board[y][x] = board[selected[0]][selected[1]]
                        board[selected[0]][selected[1]] = 0
                        winner = check_win()
                        turn = 3 - turn
                        selected = None
                    else:
                        selected = None
                elif board[y][x] == turn:
                    selected = (y, x)
    if not menu and mode == 2 and turn == 2 and winner == 0:
        pygame.time.wait(300)
        bot_move()
        winner = check_win()
        turn = 1
    draw_board()
    if winner:
        font = pygame.font.SysFont(None, 60)
        text = font.render(f'Победа {"Белых" if winner==1 else "Черных"}!', True, (0, 180, 0))
        screen.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - text.get_height()//2))
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit() 
