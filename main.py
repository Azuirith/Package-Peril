import time
import pygame
pygame.init()

# Window setup
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
TITLE = "Pygame Dash"
window = pygame.display.set_mode(size=(WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption(TITLE)

# Fixed update system
# I'm doing my own fixed update system because for some reason that I don't exactly understand I get 
# smoother movement of the spikes using this system rather than using the built in one? It still has
# occasional jitters but for the most part it looks smooth.
FPS = 144  # Doing 144 instead of standard 60 because that's what my monitor runs at.
game_update_rate = 1 / FPS
accumulator = 0
previous_time = time.time()

BACKGROUND_COLOR = (225, 225, 225)
FLOOR_COLOR = (25, 25, 25)

# Utility functions
def get_delta_time():
    global previous_time
    current_time = time.time()
    delta_time = current_time - previous_time
    previous_time = current_time
    return delta_time

def get_fixed_delta_time():
    return 1 / FPS

def set_image_color(image, color):
    for x in range(image.get_width()):
        for y in range(image.get_height()):
            color.a = image.get_at((x, y)).a
            image.set_at((x, y), color)

class Player():
    SIZE = 50
    COLOR = (100, 100, 100)
    JUMP_FORCE = 10
    GRAVITY_FORCE = 35

    def __init__(self, left, top):
        self.rect = pygame.Rect(left, top, self.SIZE, self.SIZE)
        self.is_grounded = True
        self.y_velocity = 0

    def check_for_ground(self):
        if self.rect.bottom - self.y_velocity > floor.top:
            self.rect.bottom = floor.top
            self.y_velocity = 0
            return True
        
        return False

    def jump(self):
        self.is_grounded = False
        self.y_velocity += self.JUMP_FORCE

    def update(self):
        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_SPACE] and self.is_grounded: self.jump() 

        self.y_velocity -= self.GRAVITY_FORCE * get_fixed_delta_time()
        self.is_grounded = self.check_for_ground()
        if not self.is_grounded: self.rect.top -= self.y_velocity 

class Spike():
    SIZE = 50
    COLOR = FLOOR_COLOR
    SPIKE_SPEED = 5

    def __init__(self, left, top):
        self.sprite = pygame.image.load("assets/spike.png")
        self.sprite = pygame.transform.scale(self.sprite, (self.SIZE, self.SIZE))
        set_image_color(self.sprite, pygame.Color(self.COLOR))

        self.rect = self.sprite.get_rect()
        self.rect.left = left
        self.rect.top = top

    def update(self):
        self.rect.left -= self.SPIKE_SPEED

        if self.rect.left < -self.SIZE: self.rect.left = WINDOW_WIDTH

floor = pygame.Rect(0, WINDOW_HEIGHT - 150, WINDOW_WIDTH, 150)

player = Player(125, floor.top - Player.SIZE)

spike = Spike(WINDOW_WIDTH - Spike.SIZE * 2, floor.top - Spike.SIZE)

game_running = True
while game_running:
    # Updates game once 
    delta_time = get_delta_time()
    accumulator += delta_time

    if accumulator < game_update_rate: continue
    else: accumulator -= game_update_rate

    for event in pygame.event.get():
        if event.type == pygame.QUIT: game_running = False

    # Draw scene
    window.fill(BACKGROUND_COLOR)
    pygame.draw.rect(window, FLOOR_COLOR, floor)

    player.update()
    pygame.draw.rect(window, Player.COLOR, player.rect)

    spike.update()
    window.blit(spike.sprite, spike.rect)

    pygame.display.flip()

pygame.quit()