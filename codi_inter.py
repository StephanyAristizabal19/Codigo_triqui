import pygame
from pygame.locals import *
from PIL import Image, ImageDraw, ImageFont

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

pygame.init()

FONT = pygame.font.Font(None, 100)
FONT_SMALL = pygame.font.Font(None, 40)

class Board:
    def __init__(self, screen_width, screen_height, board_size, cell_size, pil_font):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.board_size = board_size
        self.cell_size = cell_size
        self.board = [["" for _ in range(board_size)] for _ in range(board_size)]
        self.pil_font = pil_font

    def draw(self):
        image = Image.new("RGB", (self.screen_width, self.screen_height), WHITE)
        draw = ImageDraw.Draw(image)

        for i in range(1, self.board_size):
            x = self.cell_size * i
            y = self.cell_size * i
            draw.line([(x, 0), (x, self.screen_height)], fill=BLACK)
            draw.line([(0, y), (self.screen_width, y)], fill=BLACK)

        self.draw_symbols(draw)

        pygame_image = pygame.image.fromstring(image.tobytes(), image.size, image.mode)
        return pygame_image

    def draw_symbols(self, draw):
        for y in range(self.board_size):
            for x in range(self.board_size):
                if self.board[y][x] != "":
                    color = RED if self.board[y][x] == 'X' else BLUE
                    text = self.board[y][x]
                    text_width, text_height = self.pil_font.getsize(text)
                    position = (x * self.cell_size + (self.cell_size - text_width) // 2,
                                y * self.cell_size + (self.cell_size - text_height) // 2)
                    draw.text(position, text, fill=color, font=self.pil_font)

class Player:
    def __init__(self, symbol, is_computer=False):
        self.symbol = symbol
        self.is_computer = is_computer

class Game:
    def __init__(self, screen_width, screen_height, board_size):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.board_size = board_size
        self.cell_size = screen_width // board_size
        
        pygame.init()
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption("Tic Tac Toe")

        FONT_PATH = "arial.ttf"  
        try:
            self.pil_font = ImageFont.truetype(FONT_PATH, 64)
        except IOError:
            print(f"No se pudo cargar la fuente '{FONT_PATH}'. Asegúrate de que el archivo existe y la ruta es correcta.")
            exit()

        self.board = Board(screen_width, screen_height, board_size, self.cell_size, self.pil_font)
        self.players = [Player('X'), Player('O')]
        self.current_player_index = 0

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                elif event.type == MOUSEBUTTONDOWN:
                    self.handle_click(event.pos)

            self.screen.blit(self.board.draw(), (0, 0))
            pygame.display.flip()

        pygame.quit()
        
    def handle_click(self, position):
        x, y = position
        board_x = x // self.cell_size
        board_y = y // self.cell_size

        if self.board.board[board_y][board_x] == "":
            self.board.board[board_y][board_x] = self.players[self.current_player_index].symbol
            self.current_player_index = (self.current_player_index + 1) % len(self.players)

if __name__ == "__main__":
    game = Game(400, 400, 3)
    game.run()
