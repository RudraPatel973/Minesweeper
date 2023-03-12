import pygame
import random

# Define constants
WIDTH = 640
HEIGHT = 480
BOARD_SIZE = (16, 16)
BOMB_SIZE = 32
NUM_BOMBS = 40
GRAY = (192, 192, 192)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
FPS = 60

# Initialize Pygame
pygame.init()

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Minesweeper")

# Load the images
flag_img = pygame.image.load('flag.png')

# Load the font
bomb_font = pygame.font.SysFont('arial', 24)

def get_adjacent_squares(board, row, col):
    """
    Returns a list of adjacent squares on the board.
    """
    adj_squares = []
    for i in range(-1, 2):
        for j in range(-1, 2):
            if (i != 0 or j != 0) and row+i >= 0 and row+i < BOARD_SIZE[1] and col+j >= 0 and col+j < BOARD_SIZE[0]:
                adj_squares.append(board[row+i][col+j])
    return adj_squares

def generate_board():
    """
    Generates a Minesweeper board with bombs and numbers.
    """
    # Create a blank board
    board = [[0 for col in range(BOARD_SIZE[0])] for row in range(BOARD_SIZE[1])]

    # Add bombs to the board
    bombs = random.sample(range(BOARD_SIZE[0]*BOARD_SIZE[1]), NUM_BOMBS)
    for bomb in bombs:
        row = bomb // BOARD_SIZE[0]
        col = bomb % BOARD_SIZE[0]
        board[row][col] = 'B'

    # Add numbers to the board
    for row in range(BOARD_SIZE[1]):
        for col in range(BOARD_SIZE[0]):
            if board[row][col] == 'B':
                continue
            adj_squares = get_adjacent_squares(board, row, col)
            num_bombs = adj_squares.count('B')
            board[row][col] = num_bombs

    return board

def reveal_board(board, revealed_board, row, col):
    """
    Recursively reveals squares on the board.
    """
    if revealed_board[row][col]:
        return
    revealed_board[row][col] = True
    if board[row][col] == 'B':
        return
    if board[row][col] == 0:
        for i in range(-1, 2):
            for j in range(-1, 2):
                if (i != 0 or j != 0) and row+i >= 0 and row+i < BOARD_SIZE[1] and col+j >= 0 and col+j < BOARD_SIZE[0]:
                    reveal_board(board, revealed_board, row+i, col+j)

# Generate the board
board = generate_board()

# Create a blank revealed board
revealed_board = [[False for col in range(BOARD_SIZE[0])] for row in range(BOARD_SIZE[1])]

# Main game loop
game_over = False
won = False
num_flags = 0
clock = pygame.time.Clock()
while not game_over:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        # Left-click: reveal square
                        x, y = pygame.mouse.get_pos()
                        col = x // BOMB_SIZE
                        row = y // BOMB_SIZE
                        if not revealed_board[row][col]:
                            if board[row][col] == 'B':
                                # Game over
                                revealed_board[row][col] = True
                                game_over = True
                            else:
                                reveal_board(board, revealed_board, row, col)
                                # Check for win condition
                                if sum(row.count(False) for row in revealed_board) == NUM_BOMBS:
                                    won = True
                                    game_over = True
                    elif event.button == 3:
                        # Right-click: place/remove flag
                        x, y = pygame.mouse.get_pos()
                        col = x // BOMB_SIZE
                        row = y // BOMB_SIZE
                        if not revealed_board[row][col]:
                            if board[row][col] == 'B':
                                num_flags += 1
                            revealed_board[row][col] = True

# Draw the screen
screen.fill(GRAY)

# Draw the board
for row in range(BOARD_SIZE[1]):
    for col in range(BOARD_SIZE[0]):
        x = col * BOMB_SIZE
        y = row * BOMB_SIZE
        if not revealed_board[row][col]:
            pygame.draw.rect(screen, BLACK, (x, y, BOMB_SIZE, BOMB_SIZE))
            if num_flags > 0 and pygame.mouse.get_pressed()[2]:
                screen.blit(flag_img, (x, y))
                num_flags -= 1
        else:
            if board[row][col] == 'B':
                pygame.draw.circle(screen, RED, (x+BOMB_SIZE//2, y+BOMB_SIZE//2), BOMB_SIZE//2)
            else:
                pygame.draw.rect(screen, WHITE, (x, y, BOMB_SIZE, BOMB_SIZE))
                if board[row][col] > 0:
                    num_text = bomb_font.render(str(board[row][col]), True, BLACK)
                    screen.blit(num_text, (x+BOMB_SIZE//2-num_text.get_width()//2, y+BOMB_SIZE//2-num_text.get_height()//2))

# Update the display
pygame.display.update()

# Tick the clock
clock.tick(FPS)

#Show the end screen
if won:
    text = bomb_font.render("You win!", True, BLACK)
else:
    text = bomb_font.render("You lose!", True, BLACK)
    screen.blit(text, (WIDTH//2-text.get_width()//2, HEIGHT//2-text.get_height()//2))
    pygame.display.update()
    pygame.time.wait(3000)
#Quit pygame
pygame.quit()


