import pygame
import random
from settings import ColorSettings, InputSettings, PlayerSettings, ScreenSettings

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface(PlayerSettings.SIZE)
        self.image.fill(ColorSettings.YELLOW)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def input(self):
        # Keyboard input for movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= PlayerSettings.SPEED
        if keys[pygame.K_RIGHT]:
            self.rect.x += PlayerSettings.SPEED
        if keys[pygame.K_UP]:
            self.rect.y -= PlayerSettings.SPEED
        if keys[pygame.K_DOWN]:
            self.rect.y += PlayerSettings.SPEED

        # Controller input for movement
        for i in range(pygame.joystick.get_count()):
            joystick = pygame.joystick.Joystick(i)
            if joystick.get_axis(InputSettings.JOY_AXIS_LEFT_X) < -InputSettings.JOY_TRIGGER_THRESHOLD:
                self.rect.x -= PlayerSettings.SPEED
            if joystick.get_axis(InputSettings.JOY_AXIS_LEFT_X) > InputSettings.JOY_TRIGGER_THRESHOLD:
                self.rect.x += PlayerSettings.SPEED
            if joystick.get_axis(InputSettings.JOY_AXIS_LEFT_Y) < -InputSettings.JOY_TRIGGER_THRESHOLD:
                self.rect.y -= PlayerSettings.SPEED
            if joystick.get_axis(InputSettings.JOY_AXIS_LEFT_Y) > InputSettings.JOY_TRIGGER_THRESHOLD:
                self.rect.y += PlayerSettings.SPEED

    def enforce_boundaries(self, screen_width, screen_height):
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > screen_width:
            self.rect.right = screen_width
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > screen_height:
            self.rect.bottom = screen_height

    def update(self):
        self.input()
        self.enforce_boundaries(ScreenSettings.WIDTH, ScreenSettings.HEIGHT)

class Fish(pygame.sprite.Sprite):
    def __init__(self, side, size, speed):
        super().__init__()
        self.image = pygame.Surface((size, size))
        self.image.fill(ColorSettings.RED)
        self.rect = self.image.get_rect()
        
        self.speed = speed
        self.direction = 1 if side == "left" else -1
        
        # Position spawning
        if side == "left":
            self.rect.right = 0
        else:
            self.rect.left = ScreenSettings.WIDTH
            
        self.rect.y = random.randint(0, ScreenSettings.HEIGHT - size)

    def update(self):
        self.rect.x += self.speed * self.direction
        
        # Kill if off-screen
        if self.rect.right < -50 or self.rect.left > ScreenSettings.WIDTH + 50:
            self.kill()