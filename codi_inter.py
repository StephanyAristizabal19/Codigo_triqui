import pygame
from pygame.locals import *
from PIL import Image, ImageDraw

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

class Board:
    def __init__(self, screen_width, screen_height, board_size, cell_size):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.board_size = board_size
        self.cell_size = cell_size

    def draw(self):
        image = Image.new("RGB", (self.screen_width, self.screen_height), WHITE)
        draw = ImageDraw.Draw(image)

        for i in range(1, self.board_size):
            x = self.cell_size * i
            y = self.cell_size * i
            draw.line([(x, 0), (x, self.screen_height)], fill=BLACK)
            draw.line([(0, y), (self.screen_width, y)], fill=BLACK)

        pygame_image = pygame.image.fromstring(image.tobytes(), image.size, image.mode)

        return pygame_image

class Game:
    def __init__(self, screen_width, screen_height, board_size):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.board_size = board_size
        self.cell_size = screen_width // board_size
        
        pygame.init()
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption("Tic Tac Toe")

        self.board = Board(screen_width, screen_height, board_size, self.cell_size)

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False

            self.screen.blit(self.board.draw(), (0, 0))
            pygame.display.flip()

        pygame.quit()

if __name__ == "__main__":
    game = Game(400, 400, 3)
    game.run()
