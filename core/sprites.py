import pygame
import random
from settings import ColorSettings, FishSettings, InputSettings, PlayerSettings, ScreenSettings

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface(PlayerSettings.SIZE)
        self.image.fill(ColorSettings.YELLOW)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.mask = pygame.mask.from_surface(self.image)

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
        self.size = size  # stored directly for accurate area comparisons
        self.speed = speed
        self.direction = 1 if side == "left" else -1

        # "size" drives the body diamond's width. BODY_HEIGHT_RATIO squashes the
        # height below 1:1, giving that flat, horizontally-stretched fish silhouette.
        body_height = max(1, int(size * FishSettings.BODY_HEIGHT_RATIO))
        tail_width = max(1, int(size * FishSettings.TAIL_WIDTH_RATIO))
        total_width = size + tail_width

        # The vertical midpoint of the surface; both shapes' horizontal tips land here.
        center_y = body_height // 2

        # The fish is always constructed facing RIGHT first, then flipped if needed.
        #
        # Layout (left → right):
        #   [tail triangle] [body diamond →nose]
        #
        # Tail: wide end fans out to the top-left and bottom-left corners of the
        #       surface; the pointed tip aims right to meet the diamond's left vertex.
        # Body: a flat diamond whose left tip shares the tail's point, and whose
        #       right tip is the nose of the fish pointing in the direction of travel.
        self.image = pygame.Surface((total_width, body_height), pygame.SRCALPHA)

        tail_points = [
            (0, 0),                  # top-left corner — wide end of the tail fan
            (0, body_height),        # bottom-left corner — wide end of the tail fan
            (tail_width, center_y),  # tip pointing right, connecting to the body
        ]
        body_points = [
            (tail_width, center_y),              # left tip — shared with the tail tip
            (tail_width + size // 2, 0),         # top-center peak of the diamond
            (total_width, center_y),             # right tip — the nose of the fish
            (tail_width + size // 2, body_height),  # bottom-center peak of the diamond
        ]
        pygame.draw.polygon(self.image, ColorSettings.RED, tail_points)
        pygame.draw.polygon(self.image, ColorSettings.RED, body_points)

        # Left-moving fish face left. Mirroring horizontally keeps the nose pointed
        # in the direction of travel and the tail fanning out behind it.
        if self.direction == -1:
            self.image = pygame.transform.flip(self.image, True, False)

        self.rect = self.image.get_rect()
        # Build a pixel mask from the drawn surface so collision checks ignore
        # the transparent corners of the bounding box.
        self.mask = pygame.mask.from_surface(self.image)

        # Spawn just off the edge of the screen on the correct side.
        if side == "left":
            self.rect.right = 0
        else:
            self.rect.left = ScreenSettings.WIDTH

        self.rect.y = random.randint(0, ScreenSettings.HEIGHT - body_height)

    def update(self):
        self.rect.x += self.speed * self.direction
        
        # Kill if off-screen
        if self.rect.right < -50 or self.rect.left > ScreenSettings.WIDTH + 50:
            self.kill()