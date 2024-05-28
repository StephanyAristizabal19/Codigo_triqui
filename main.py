import pygame
import random
import sys

pygame.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
font = pygame.font.Font(None, 100)
font_small = pygame.font.Font(None, 40)

class Player:
    def __init__(self, symbol, is_computer=False):
        self.symbol = symbol
        self.is_computer = is_computer

class Board:
    def __init__(self):
        self.board = [["" for _ in range(3)] for _ in range(3)]
        self.winning_line = None

    def reset(self):
        self.board = [["" for _ in range(3)] for _ in range(3)]
        self.winning_line = None

    def draw(self, screen):
        screen.fill(WHITE)
        for x in range(1, 3):
            pygame.draw.line(screen, BLACK, (x * 133, 0), (x * 133, 400), 3)
            pygame.draw.line(screen, BLACK, (0, x * 133), (400, x * 133), 3)
        self.draw_symbols(screen)

    def draw_symbols(self, screen):
        for y in range(3):
            for x in range(3):
                if self.board[y][x] != "":
                    color = RED if self.board[y][x] == 'X' else BLUE
                    text = font.render(self.board[y][x], True, color)
                    screen.blit(text, (x * 133 + 33, y * 133 + 33))

    def check_winner(self):
        for row in range(3):
            if self.board[row][0] == self.board[row][1] == self.board[row][2] != "":
                self.winning_line = ((0, row), (2, row))
                return self.board[row][0]
        for col in range(3):
            if self.board[0][col] == self.board[1][col] == self.board[2][col] != "":
                self.winning_line = ((col, 0), (col, 2))
                return self.board[0][col]
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != "":
            self.winning_line = ((0, 0), (2, 2))
            return self.board[0][0]
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != "":
            self.winning_line = ((2, 0), (0, 2))
            return self.board[0][2]
        return None

    def handle_click(self, x, y, symbol):
        if self.board[y][x] == "":
            self.board[y][x] = symbol
            return True
        return False

    def draw_winning_line(self, screen, winner):
        color = RED if winner == 'X' else BLUE
        start_pos = (self.winning_line[0][0] * 133 + 67, self.winning_line[0][1] * 133 + 67)
        end_pos = (self.winning_line[1][0] * 133 + 67, self.winning_line[1][1] * 133 + 67)
        pygame.draw.line(screen, color, start_pos, end_pos, 5)
        pygame.display.flip()

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((400, 400))
        pygame.display.set_caption("Tic Tac Toe")
        self.board = Board()
        self.player = Player('X')
        self.computer = Player('O', is_computer=True)
        self.current_player = self.player
        self.computer_starts = False

    def pc_move(self):
        # Check if computer can win in the next move
        for y in range(3):
            for x in range(3):
                if self.board.board[y][x] == "":
                    self.board.board[y][x] = self.computer.symbol
                    if self.board.check_winner() == self.computer.symbol:
                        return
                    self.board.board[y][x] = ""

        # Check if player can win in the next move and block them
        for y in range(3):
            for x in range(3):
                if self.board.board[y][x] == "":
                    self.board.board[y][x] = self.player.symbol
                    if self.board.check_winner() == self.player.symbol:
                        self.board.board[y][x] = self.computer.symbol
                        return
                    self.board.board[y][x] = ""

        # Make a move in the best available spot
        empty_cells = [(x, y) for y in range(3) for x in range(3) if self.board.board[y][x] == ""]
        if empty_cells:
            move = random.choice(empty_cells)
            self.board.handle_click(*move, self.computer.symbol)

    def reset_game(self):
        self.board.reset()
        if self.computer_starts:
            self.current_player = self.computer
        else:
            self.current_player = self.player

    def check_game_state(self):
        winner = self.board.check_winner()
        if winner:
            self.board.draw(self.screen)  # Asegurarse de que la última ficha se dibuje
            pygame.display.flip()
            print(f"{winner} wins!")
            self.board.draw_winning_line(self.screen, winner)
            pygame.time.wait(2000)
            if winner == self.computer.symbol:
                self.computer_starts = True
            else:
                self.computer_starts = False
            self.reset_game()
        elif all(all(cell != "" for cell in row) for row in self.board.board):
            self.board.draw(self.screen)  # Asegurarse de que la última ficha se dibuje
            pygame.display.flip()
            print("It's a tie!")
            pygame.time.wait(2000)
            self.computer_starts = not self.computer_starts
            self.reset_game()
        else:
            self.current_player = self.computer if self.current_player == self.player else self.player

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.current_player == self.player:
                        mouse_x, mouse_y = event.pos
                        clicked_row = mouse_y // 133
                        clicked_col = mouse_x // 133
                        if self.board.handle_click(clicked_col, clicked_row, self.player.symbol):
                            self.board.draw(self.screen)  # Dibuja el tablero después de cada movimiento
                            pygame.display.flip()  # Actualiza la pantalla inmediatamente
                            self.check_game_state()
            if self.current_player == self.computer and running:
                pygame.time.wait(500)  # Añadir una pequeña pausa para la sensación de "pensar"
                self.pc_move()
                self.board.draw(self.screen)  # Dibuja el tablero después de cada movimiento
                pygame.display.flip()  # Actualiza la pantalla inmediatamente
                self.check_game_state()

            self.board.draw(self.screen)
            pygame.display.flip()
        pygame.quit()

if __name__ == "__main__":
    Game().run()
