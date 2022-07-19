import math
import random
import time
import pygame
pygame.init()

class Game():
    # Window configuration
    WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
    TITLE = "Package Peril"

    # Text configuration (The pygame font system is weird)
    NORMAL_FONT = pygame.font.Font("assets/fonts/Bungee-Regular.ttf", 24)
    MEDIUM_FONT = pygame.font.Font("assets/fonts/Bungee-Regular.ttf", 48)
    LARGE_FONT = pygame.font.Font("assets/fonts/Bungee-Regular.ttf", 72)
    TEXT_OFFSET_FROM_BORDER = 16

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
        self.on_main_menu = True

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
        return pygame.Rect(0, self.WINDOW_HEIGHT - 150, self.WINDOW_WIDTH, 150)

    def create_player(self):
        return Player(125, self.floor.top - Player.HEIGHT)
    
    def create_box_handler(self):
        return BoxHandler()

    def draw_scene(self):
        self.window.fill(self.BACKGROUND_COLOR)
        pygame.draw.rect(self.window, self.FLOOR_COLOR, self.floor)

    def draw_objects(self):
        self.window.blit(self.player.sprite, self.player.rect)
        self.window.blit(self.box_handler.current_box.sprite, self.box_handler.current_box.rect)

    def draw_UI(self):
        if self.on_main_menu:
            title_text_string = self.TITLE
            title_text_UI = self.LARGE_FONT.render(title_text_string, True, self.TEXT_COLOR)
            title_text_x = self.WINDOW_WIDTH / 2 - title_text_UI.get_width() / 2
            title_text_y = self.WINDOW_HEIGHT / 2 - title_text_UI.get_height() * 1.5
            self.window.blit(title_text_UI, (title_text_x, title_text_y))

            play_text_string = "Press SPACE to start"
            play_text_UI = self.NORMAL_FONT.render(play_text_string, True, self.TEXT_COLOR)
            play_text_x = self.WINDOW_WIDTH / 2 - play_text_UI.get_width() / 2
            play_text_y = self.WINDOW_HEIGHT / 2 - play_text_UI.get_height() / 2
            self.window.blit(play_text_UI, (play_text_x, play_text_y))
        else:
            # The unnecessary amount of variables here is to shorten the lines because they were originally
            # too long
            score_text_string = f"Score: {self.player.score}"
            score_text_UI = self.NORMAL_FONT.render(score_text_string, True, self.TEXT_COLOR)
            score_text_x = self.TEXT_OFFSET_FROM_BORDER
            score_text_y = self.TEXT_OFFSET_FROM_BORDER
            self.window.blit(score_text_UI, (score_text_x, score_text_y))

            speed_text_string = f"Boxes until speed increase: {self.box_handler.boxes_until_speed_change()}"
            speed_text_UI = self.NORMAL_FONT.render(speed_text_string, True, self.TEXT_COLOR)
            speed_text_x = self.TEXT_OFFSET_FROM_BORDER
            speed_text_y = self.TEXT_OFFSET_FROM_BORDER * 2 + score_text_UI.get_size()[1]
            self.window.blit(speed_text_UI, (speed_text_x, speed_text_y))

            if self.player.has_been_hit:
                restart_text_string = "Press R to restart"
                restart_text_UI = self.MEDIUM_FONT.render(restart_text_string, True, self.TEXT_COLOR)
                restart_text_x = self.WINDOW_WIDTH / 2 - restart_text_UI.get_width() / 2
                restart_text_y = self.WINDOW_HEIGHT / 2 - restart_text_UI.get_height() / 2
                self.window.blit(restart_text_UI, (restart_text_x, restart_text_y))

    def update_objects(self):
        if self.player.has_been_hit: return
        self.player.update()

        self.box_handler.current_box.update()
        if self.box_handler.current_box.rect.colliderect(self.player.rect): self.player.has_been_hit = True

    def initialize(self):
        self.box_handler.spawn_box()

    def restart(self):
        self.player.score = 1
        self.player.rect.bottom = self.floor.top
        self.box_handler.reset()

    def update(self):
        # Creates fixed update rate
        delta_time = self.get_delta_time()
        self.accumulator += delta_time

        if self.accumulator < self.UPDATE_RATE: return
        else: self.accumulator -= self.UPDATE_RATE

        for event in pygame.event.get():
            if event.type == pygame.QUIT: self.running = False

        self.draw_scene()
        self.draw_UI()

        keys_pressed = pygame.key.get_pressed()

        # Updates the game based on whether it's on the main menu or not
        if self.on_main_menu:
            if keys_pressed[pygame.K_SPACE]: self.on_main_menu = False
        else:
            if self.player.has_been_hit: 
                if keys_pressed[pygame.K_r]: 
                    self.restart()
                    self.player.has_been_hit = False
                
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

    def will_hit_ground(self):
        return self.rect.bottom - self.y_velocity > game.floor.top

    def jump(self):
        self.is_grounded = False
        self.y_velocity += self.JUMP_FORCE

    def update(self):
        if self.has_been_hit: return

        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_SPACE] and self.is_grounded: self.jump() 

        self.y_velocity -= self.GRAVITY_FORCE * game.UPDATE_RATE
        self.is_grounded = self.will_hit_ground()
        if self.is_grounded: 
            self.rect.bottom = game.floor.top
            self.y_velocity = 0
        else: 
            self.rect.top -= self.y_velocity 
            
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

class BoxHandler():
    BOX_BASE_SPEED = 5
    BOX_MAX_SPEED = 15
    SPEED_CHANGE_FREQUENCY = 5

    def __init__(self):
        self.current_box = None
        self.current_speed = self.BOX_BASE_SPEED
        self.boxes_since_speed_changed = 0 
        self.speed_change_counter = 0

    def boxes_until_speed_change(self):
        return self.SPEED_CHANGE_FREQUENCY - self.boxes_since_speed_changed

    def add_randomness_to_speed(self):
        speed_randomness = random.randint(math.floor(-self.current_speed / 6), math.floor(self.current_speed / 6))
        return speed_randomness

    def reset(self):
        self.current_speed = self.BOX_BASE_SPEED
        self.boxes_since_speed_changed = 0
        self.speed_change_counter = 0
        self.spawn_box()

    def spawn_box(self):
        self.boxes_since_speed_changed += 1
        if self.boxes_since_speed_changed >= self.SPEED_CHANGE_FREQUENCY:
            self.speed_change_counter += 1
            self.boxes_since_speed_changed = 0

            box_speed_increment = (self.speed_change_counter / (self.speed_change_counter + self.BOX_MAX_SPEED))
            self.current_speed = self.BOX_MAX_SPEED * box_speed_increment + self.BOX_BASE_SPEED  # 10 is an arbitrary number

        box_type = random.randint(1, 4)
        new_box = Box(self.current_speed + self.add_randomness_to_speed())

        match box_type:
            # Medium box
            case 1:
                new_box.rect.width = 96
                new_box.rect.height = 96
                new_box.sprite = game.SQUARE_BOX_SPRITE
            # Big box
            case 2:
                new_box.rect.width = 128
                new_box.rect.height = 128
                new_box.sprite = game.SQUARE_BOX_SPRITE

            # Tall box
            case 3: 
                new_box.rect.width = 64
                new_box.rect.height = 128
                new_box.sprite = game.TALL_BOX_SPRITE

            # Long box
            case 4:
                new_box.rect.width = 160
                new_box.rect.height = 64
                new_box.sprite = game.LONG_BOX_SPRITE
        
        new_box.sprite = pygame.transform.scale(new_box.sprite, (new_box.rect.width, new_box.rect.height))
        new_box.rect.left = game.WINDOW_WIDTH
        new_box.rect.top = game.floor.top - new_box.rect.height
        self.current_box = new_box

game = Game()
game.initialize()

while game.running: game.update()

pygame.quit()