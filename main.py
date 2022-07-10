from re import L
from sre_constants import JUMP
import pygame
pygame.init()

WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
TITLE = "Pygame Dash"
window = pygame.display.set_mode(size=(WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption(TITLE)

FPS = 60
clock = pygame.time.Clock()

BACKGROUND_COLOR = (225, 225, 225)
FLOOR_COLOR = (25, 25, 25)

def get_delta_time():
    return 1/FPS

class Player():
    SIZE = 50
    COLOR = (100, 100, 100)
    JUMP_FORCE = 10


    def __init__(self, left, top):
        self.rect = pygame.Rect(left, top, self.SIZE, self.SIZE)
        self.is_grounded = True
        self.y_velocity = 0

    def jump(self):
        self.is_grounded = False
        self.y_velocity += self.JUMP_FORCE

    def update(self):
        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_SPACE] and self.is_grounded: self.jump()  

floor = pygame.Rect(0, WINDOW_HEIGHT - 150, WINDOW_WIDTH, 150)

player = Player(100, floor.top - Player.SIZE)

game_running = True
while game_running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT: game_running = False

    # Draw scene
    window.fill(BACKGROUND_COLOR)
    pygame.draw.rect(window, FLOOR_COLOR, floor)

    player.update()
    pygame.draw.rect(window, Player.COLOR, player.rect)

    pygame.display.flip()

pygame.quit()