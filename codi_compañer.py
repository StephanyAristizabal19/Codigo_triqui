import pygame
pygame.init()

screen = pygame.display.set_mode((300, 300))
pygame.display.set_caption("Tic Tac Toe")
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
font = pygame.font.Font(None, 100)

def draw_grid():
    screen.fill(WHITE)
    for x in range(1, 3):
        pygame.draw.line(screen, BLACK, (x * 100, 0), (x * 100, 300), 3)
        pygame.draw.line(screen, BLACK, (0, x * 100), (300, x * 100), 3)
        
board = [["" for _ in range(3)] for _ in range(3)]
current_player = "X"

def draw_symbols():
    for y in range(3):
        for x in range(3):
            if board[y][x] != "":
                text = font.render(board[y][x], True, BLACK)
                screen.blit(text, (x * 100 + 25, y * 100 + 25))
                
def check_winner():
    for row in board:
        if row[0] == row[1] == row[2] != "":
            return row[0]
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] != "":
            return board[0][col]
    if board[0][0] == board[1][1] == board[2][2] != "" or board[0][2] == board[1][1] == board[2][0] != "":
        return board[1][1]
    return None

def handle_click(x, y):
    global current_player
    if board[y][x] == "":
        board[y][x] = current_player
        current_player = "O" if current_player == "X" else "X"
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            clicked_row = mouse_y // 100
            clicked_col = mouse_x // 100
            handle_click(clicked_col, clicked_row)

    draw_grid()
    draw_symbols()
    winner = check_winner()
    if winner:
        print(f"{winner} wins!")
        running = False

    pygame.display.flip()
pygame.quit()