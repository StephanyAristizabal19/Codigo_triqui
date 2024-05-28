import pygame
import random
import sys

pygame.init()

# Configuración de pantalla
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Triqui con Problemas Matemáticos')

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Fuentes
font = pygame.font.Font(None, 36)

class MathProblem:
    def _init_(self):
        self.problem, self.solution = self.generate_problem()

    def generate_problem(self):
        num1 = random.randint(1, 10)
        num2 = random.randint(1, 10)
        operation = random.choice(['+', '-'])
        if operation == '+':
            solution = num1 + num2
        else:
            solution = num1 - num2
        problem = f"{num1} {operation} {num2} = ?"
        return problem, solution

    def draw(self, screen):
        problem_surface = font.render(self.problem, True, BLACK)
        screen.blit(problem_surface, (WIDTH // 2 - problem_surface.get_width() // 2, HEIGHT // 2 - problem_surface.get_height() // 2))

class TicTacToe:
    def _init_(self):
        self.board = ['' for _ in range(9)]
        self.current_player = 'X'
        self.winner = None

    def draw(self, screen):
        for row in range(3):
            for col in range(3):
                cell = self.board[row * 3 + col]
                x = col * 100 + 100
                y = row * 100 + 50
                pygame.draw.rect(screen, BLACK, (x, y, 100, 100), 3)
                if cell:
                    cell_surface = font.render(cell, True, RED if cell == 'X' else BLUE)
                    screen.blit(cell_surface, (x + 50 - cell_surface.get_width() // 2, y + 50 - cell_surface.get_height() // 2))

    def check_winner(self):
        winning_combinations = [(0, 1, 2), (3, 4, 5), (6, 7, 8), 
                                (0, 3, 6), (1, 4, 7), (2, 5, 8), 
                                (0, 4, 8), (2, 4, 6)]
        for combo in winning_combinations:
            if self.board[combo[0]] == self.board[combo[1]] == self.board[combo[2]] != '':
                self.winner = self.board[combo[0]]
                return True
        if '' not in self.board:
            self.winner = 'Draw'
            return True
        return False

    def make_move(self, pos):
        if self.board[pos] == '':
            self.board[pos] = self.current_player
            if not self.check_winner():
                self.current_player = 'O' if self.current_player == 'X' else 'X'

class Game:
    def _init_(self):
        self.math_problem = MathProblem()
        self.tic_tac_toe = TicTacToe()
        self.game_started = False
        self.player_solution = ''

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if self.game_started:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    x, y = event.pos
                    col = (x - 100) // 100
                    row = (y - 50) // 100
                    if 0 <= col < 3 and 0 <= row < 3:
                        self.tic_tac_toe.make_move(row * 3 + col)
            else:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        try:
                            if int(self.player_solution) == self.math_problem.solution:
                                self.game_started = True
                        except ValueError:
                            pass
                        self.player_solution = ''
                    elif event.key == pygame.K_BACKSPACE:
                        self.player_solution = self.player_solution[:-1]
                    else:
                        self.player_solution += event.unicode

    def draw(self):
        screen.fill(WHITE)
        if self.game_started:
            self.tic_tac_toe.draw(screen)
            if self.tic_tac_toe.winner:
                winner_text = f"Winner: {self.tic_tac_toe.winner}" if self.tic_tac_toe.winner != 'Draw' else "It's a Draw!"
                winner_surface = font.render(winner_text, True, BLACK)
                screen.blit(winner_surface, (WIDTH // 2 - winner_surface.get_width() // 2, 20))
        else:
            self.math_problem.draw(screen)
            solution_surface = font.render(self.player_solution, True, BLACK)
            screen.blit(solution_surface, (WIDTH // 2 - solution_surface.get_width() // 2, HEIGHT // 2 + 50))

    def run(self):
        while True:
            self.handle_events()
            self.draw()
            pygame.display.flip()

if __name__ == "__main__":
    game = Game()
    game.run()