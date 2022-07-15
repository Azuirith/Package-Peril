import random
import time
import pygame
pygame.init()

class Game():
    # Window configuration
    WINDOW_WIDTH = 1280
    WINDOW_HEIGHT = 720
    TITLE = "Package Peril"

    # Text configuration
    FONT = pygame.font.Font("assets/fonts/Bungee-Regular.ttf", 24)
    TEXT_OFFSET_FROM_WINDOW = 16

    # Update rate configuration
    FPS = 144
    UPDATE_RATE = 1 / FPS

    # Sprite initialization
    SQUARE_BOX_SPRITE = pygame.image.load("assets/sprites/square_box.png")
    LONG_BOX_SPRITE = pygame.image.load("assets/sprites/long_box.png")
    TALL_BOX_SPRITE = pygame.image.load("assets/sprites/tall_box.png")

    # Color configuration
    BACKGROUND_COLOR = (50, 50, 50)
    FLOOR_COLOR = (25, 25, 25)
    TEXT_COLOR = (255, 255, 255)

    def __init__(self):
        self.window = self.create_window()
        self.floor = self.create_floor()
        self.player = self.create_player()
        self.box_handler = self.create_box_handler()

        self.running = True
        self.accumulator = 0

        self.previous_time = time.time()  # Used for the get_delta_time method

    def get_delta_time(self):
        current_time = time.time()
        delta_time = current_time - self.previous_time
        self.previous_time = current_time
        return delta_time

    def create_window(self):
        window = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        pygame.display.set_caption(self.TITLE)
        pygame.display.set_icon(self.SQUARE_BOX_SPRITE)
        return window

    def create_floor(self):
        floor = pygame.Rect(0, self.WINDOW_HEIGHT - 150, self.WINDOW_WIDTH, 150)
        return floor

    def create_player(self):
        player = Player(125, self.floor.top - Player.HEIGHT)
        return player
    
    def create_box_handler(self):
        box_handler = BoxHandler()
        return box_handler

    def draw_scene(self):
        self.window.fill(self.BACKGROUND_COLOR)
        pygame.draw.rect(self.window, self.FLOOR_COLOR, self.floor)

    def draw_objects(self):
        self.window.blit(self.player.sprite, self.player.rect)
        self.window.blit(self.box_handler.boxes[0].sprite, self.box_handler.boxes[0].rect)

    def draw_UI(self):
        score_text = self.FONT.render(f"Score: {self.player.score}", True, self.TEXT_COLOR)
        self.window.blit(score_text, (self.TEXT_OFFSET_FROM_WINDOW, self.TEXT_OFFSET_FROM_WINDOW))

        speed_increase_text = self.FONT.render(f"Boxes until speed increase: {self.box_handler.calculate_boxes_until_speed_change()}", True, self.TEXT_COLOR)
        self.window.blit(speed_increase_text, (self.TEXT_OFFSET_FROM_WINDOW, self.TEXT_OFFSET_FROM_WINDOW * 2 + score_text.get_size()[1]))

    def update_objects(self):
        if self.player.has_been_hit: return

        self.player.update()

        currentBox = self.box_handler.boxes[0]
        currentBox.update()
        if currentBox.rect.colliderect(self.player.rect): self.player.has_been_hit = True

    def initialize(self):
        self.box_handler.spawn_box()

    def update(self):
        self.draw_scene()
        self.draw_UI()
        self.update_objects()
        self.draw_objects()

        pygame.display.flip()

class Player():
    WIDTH, HEIGHT = 64, 64
    JUMP_FORCE = 10
    GRAVITY_FORCE = 35

    def __init__(self, left, top):
        self.sprite = pygame.image.load("assets/sprites/square_box.png")
        self.sprite = pygame.transform.scale(self.sprite, (self.WIDTH, self.HEIGHT))

        self.rect = self.sprite.get_rect()
        self.rect.left = left
        self.rect.top = top

        self.is_grounded = True
        self.has_been_hit = False
        
        self.y_velocity = 0
        
        self.score = 1

    def check_for_ground(self):
        if self.rect.bottom - self.y_velocity > game.floor.top:
            self.rect.bottom = game.floor.top
            self.y_velocity = 0
            return True
        
        return False

    def jump(self):
        self.is_grounded = False
        self.y_velocity += self.JUMP_FORCE

    def update(self):
        if self.has_been_hit: return

        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_SPACE] and self.is_grounded: self.jump() 

        self.y_velocity -= self.GRAVITY_FORCE * game.UPDATE_RATE
        self.is_grounded = self.check_for_ground()
        if not self.is_grounded: self.rect.top -= self.y_velocity 

class Box():
    # Initializes the box with default values so that the method in the BoxHandler can customize the box
    def __init__(self, speed):
        self.sprite = None
        self.rect = pygame.Rect(0, 0, 0, 0)
        self.speed = speed

        self.can_add_to_score = True

    def update(self):
        self.rect.left -= self.speed
        if self.rect.left < -self.rect.width: 
            game.player.score += 1
            game.box_handler.spawn_box()
            game.box_handler.boxes.remove(self)

class BoxHandler():
    BOX_BASE_SPEED = 5
    BOX_MAX_SPEED = 15
    SPEED_CHANGE_FREQUENCY = 5

    def __init__(self):
        self.boxes = []
        self.current_box_speed = self.BOX_BASE_SPEED
        self.boxes_since_frequency_changed = 0 
        self.times_speed_changed = 0

    def calculate_boxes_until_speed_change(self):
        return self.SPEED_CHANGE_FREQUENCY - self.boxes_since_frequency_changed

    def spawn_box(self):
        self.boxes_since_frequency_changed += 1
        if self.boxes_since_frequency_changed >= self.SPEED_CHANGE_FREQUENCY:
            self.times_speed_changed += 1
            self.boxes_since_frequency_changed = 0
            self.current_box_speed = self.BOX_MAX_SPEED * (self.times_speed_changed / (self.times_speed_changed + self.BOX_MAX_SPEED)) + self.BOX_BASE_SPEED  # 10 is an arbitrary number
 
        box_type = random.randint(1, 4)
        newBox = Box(self.current_box_speed)

        match box_type:
            # Medium box
            case 1:
                newBox.rect.width = 96
                newBox.rect.height = 96
                newBox.sprite = game.SQUARE_BOX_SPRITE
            # Big box
            case 2:
                newBox.rect.width = 128
                newBox.rect.height = 128
                newBox.sprite = game.SQUARE_BOX_SPRITE

            # Tall box
            case 3: 
                newBox.rect.width = 64
                newBox.rect.height = 128
                newBox.sprite = game.TALL_BOX_SPRITE

            # Long box
            case 4:
                newBox.rect.width = 160
                newBox.rect.height = 64
                newBox.sprite = game.LONG_BOX_SPRITE
        
        newBox.sprite = pygame.transform.scale(newBox.sprite, (newBox.rect.width, newBox.rect.height))
        newBox.rect.left = game.WINDOW_WIDTH
        newBox.rect.top = game.floor.top - newBox.rect.height
        self.boxes.append(newBox)

game = Game()
game.initialize()

while game.running:
    delta_time = game.get_delta_time()
    game.accumulator += delta_time

    if game.accumulator < game.UPDATE_RATE: continue
    else: game.accumulator -= game.UPDATE_RATE

    for event in pygame.event.get():
        if event.type == pygame.QUIT: game.running = False

    game.update()

pygame.quit()