import pygame
import random
import sys
import time

pygame.init()

# Definir colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Definir fuentes
font = pygame.font.Font(None, 100)
font_small = pygame.font.Font(None, 40)

# Generar problema matemático
def generar_problema_matematico():
    operadores = ['+', '-', '*', '/']
    operador = random.choice(operadores)
    
    if operador == '/':
        divisor = random.randint(1, 10)
        numero1 = divisor * random.randint(1, 10)
        numero2 = divisor
    else:
        numero1 = random.randint(1, 100)
        numero2 = random.randint(1, 100)
    
    problema = f"{numero1} {operador} {numero2}"
    resultado = eval(problema)
    return problema, resultado

# Clase Jugador
class Player:
    def __init__(self, symbol, is_computer=False):
        self.symbol = symbol
        self.is_computer = is_computer

# Clase Tablero
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
            pygame.draw.line(screen, BLACK, (x * 100 + 150, 150), (x * 100 + 150, 450), 5)
            pygame.draw.line(screen, BLACK, (150, x * 100 + 150), (450, x * 100 + 150), 5)
        self.draw_symbols(screen)

    def draw_symbols(self, screen):
        for y in range(3):
            for x in range(3):
                if self.board[y][x] != "":
                    color = RED if self.board[y][x] == 'X' else BLUE
                    text = font.render(self.board[y][x], True, color)
                    screen.blit(text, (x * 100 + 165, y * 100 + 165))

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
        start_pos = (self.winning_line[0][0] * 100 + 200, self.winning_line[0][1] * 100 + 200)
        end_pos = (self.winning_line[1][0] * 100 + 200, self.winning_line[1][1] * 100 + 200)
        pygame.draw.line(screen, color, start_pos, end_pos, 10)
        pygame.display.flip()

# Clase Juego
class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((1100, 600))  # Ventana del juego más ancha
        pygame.display.set_caption("Tic Tac Toe")
        self.board = Board()
        self.player = Player('X')
        self.computer = Player('O', is_computer=True)
        self.current_player = self.player
        self.computer_starts = False
        self.player_score = 0
        self.computer_score = 0

    def pc_move(self):
        for y in range(3):
            for x in range(3):
                if self.board.board[y][x] == "":
                    self.board.board[y][x] = self.computer.symbol
                    if self.board.check_winner() == self.computer.symbol:
                        return
                    self.board.board[y][x] = ""

        for y in range(3):
            for x in range(3):
                if self.board.board[y][x] == "":
                    self.board.board[y][x] = self.player.symbol
                    if self.board.check_winner() == self.player.symbol:
                        self.board.board[y][x] = self.computer.symbol
                        return
                    self.board.board[y][x] = ""

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
                self.computer_score += 1
                self.computer_starts = True
            else:
                self.player_score += 1
                self.computer_starts = False
            self.mostrar_mensaje("Resultado del Juego", f"{self.player.symbol} vs {self.computer.symbol}", f"Ganador: {winner}", "¡Felicidades!")
            self.reset_game()
        elif all(all(cell != "" for cell in row) for row in self.board.board):
            self.board.draw(self.screen)  # Asegurarse de que la última ficha se dibuje
            pygame.display.flip()
            print("It's a tie!")
            pygame.time.wait(2000)
            self.mostrar_mensaje("Resultado del Juego", f"{self.player.symbol} vs {self.computer.symbol}", "Empate", "¡Intenta de nuevo!")
            self.computer_starts = not self.computer_starts
            self.reset_game()
        else:
            self.current_player = self.computer if self.current_player == self.player else self.player

    def mostrar_mensaje(self, titulo, mensaje_jugadores, mensaje_ganador, mensaje_puntaje):
        # Crear una nueva superficie para el mensaje
        mensaje_surf = pygame.Surface((400, 600))
        mensaje_surf.fill(BLUE)

        # Crear los textos
        titulo_surf = font_small.render(titulo, True, BLACK)
        mensaje_jugadores_surf = font_small.render(mensaje_jugadores, True, BLACK)
        mensaje_ganador_surf = font_small.render(mensaje_ganador, True, BLACK)
        mensaje_puntaje_surf = font_small.render(mensaje_puntaje, True, BLACK)
        boton_surf = font_small.render("Aceptar", True, WHITE)
        boton_rect = pygame.Rect(150, 500, 135, 50)

        # Dibujar los textos en la superficie del mensaje
        mensaje_surf.blit(titulo_surf, (20, 20))
        mensaje_surf.blit(mensaje_jugadores_surf, (20, 120))
        mensaje_surf.blit(mensaje_ganador_surf, (20, 220))
        mensaje_surf.blit(mensaje_puntaje_surf, (20, 320))
        pygame.draw.rect(mensaje_surf, BLACK, boton_rect)
        mensaje_surf.blit(boton_surf, (160, 510))

        # Obtener el rectángulo de la superficie del mensaje y colocarlo al lado izquierdo
        mensaje_rect = mensaje_surf.get_rect(topleft=(50, 0))

        # Esperar a que el usuario haga clic en el botón para cerrar el mensaje
        esperando = True
        while esperando:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if boton_rect.collidepoint(event.pos[0] - mensaje_rect.x, event.pos[1] - mensaje_rect.y):
                        esperando = False

            self.screen.blit(mensaje_surf, mensaje_rect.topleft)
            pygame.display.flip()

    def mostrar_problema_matematico(self):
        problema, resultado = generar_problema_matematico()

        # Obtener tamaño de pantalla
        info_object = pygame.display.Info()
        screen_width = info_object.current_w
        screen_height = info_object.current_h

        # Tamaño de la ventana del problema matemático
        problem_window_width = 300
        problem_window_height = 200

        # Calcular la posición de la ventana centrada
        problem_window_x = (screen_width - problem_window_width) // 2
        problem_window_y = (screen_height - problem_window_height) // 2

        root = pygame.display.set_mode((problem_window_width, problem_window_height))
        pygame.display.set_caption("Problema Matemático")

        start_time = time.time()
        user_input = ""
        while True:
            elapsed_time = time.time() - start_time
            if elapsed_time > 10:
                return False

            root.fill(WHITE)
            text = font_small.render(f"Resuelve: {problema}", True, BLACK)
            root.blit(text, (20, 50))
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.unicode.isdigit() or event.unicode in ['-', '.']:
                        user_input += event.unicode
                    elif event.key == pygame.K_RETURN:
                        try:
                            if float(user_input) == resultado:
                                return True
                            else:
                                return False
                        except ValueError:
                            user_input = ""

            root.fill(WHITE)
            text = font_small.render(f"Resuelve: {problema}", True, BLACK)
            root.blit(text, (20, 50))
            input_surface = font_small.render(user_input, True, BLACK)
            root.blit(input_surface, (20, 100))
            pygame.display.flip()

    def run(self):
        if self.mostrar_problema_matematico():
            self.screen = pygame.display.set_mode((1100, 600))  # Restaurar tamaño de la ventana del juego
            running = True
            while running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if self.current_player == self.player:
                            mouse_x, mouse_y = event.pos
                            clicked_row = (mouse_y - 150) // 100
                            clicked_col = (mouse_x - 150) // 100
                            if 0 <= clicked_row < 3 and 0 <= clicked_col < 3:
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
                self.draw_score()  # Dibujar el puntaje
                pygame.display.flip()
            pygame.quit()
        else:
            print("Tiempo excedido o respuesta incorrecta. Juego terminado.")
            self.current_player = self.computer  # Cambiar el turno al computador
            self.run()  # Reiniciar el juego y dejar que el computador juegue primero

    def draw_score(self):
        # Crear un fondo blanco para la sección del puntaje
        score_bg_rect = pygame.Rect(800, 0, 300, 600)
        pygame.draw.rect(self.screen, WHITE, score_bg_rect)

        # Mostrar el puntaje de cada jugador
        player_score_text = font_small.render(f"Jugador: {self.player_score}", True, BLACK)
        computer_score_text = font_small.render(f"Computadora: {self.computer_score}", True, BLACK)
        self.screen.blit(player_score_text, (850, 200))
        self.screen.blit(computer_score_text, (850, 300))

if __name__ == "__main__":
    Game().run()

