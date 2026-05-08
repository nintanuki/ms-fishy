import pygame
import random
from core.sprites import Fish
from settings import FishSettings, ColorSettings

class FishManager:
    def __init__(self, sprite_group):
        self.sprite_group = sprite_group
        self.spawn_timer = 0

    def update(self, player):
        self.spawn_timer += 1
        if self.spawn_timer >= FishSettings.SPAWN_RATE:
            self.spawn_fish()
            self.spawn_timer = 0
        
        self.check_collisions(player)

    def spawn_fish(self):
        side = random.choice(["left", "right"])
        size = random.randint(FishSettings.MIN_SIZE, FishSettings.MAX_SIZE)
        speed = random.randint(FishSettings.MIN_SPEED, FishSettings.MAX_SPEED)
        
        new_fish = Fish(side, size, speed)
        self.sprite_group.add(new_fish)

    def check_collisions(self, player):
        # We use pygame.sprite.spritecollide with a custom callback or manual loop
        collided_fish = pygame.sprite.spritecollide(player, self.sprite_group, False)
        
        for fish in collided_fish:
            player_area = player.rect.width * player.rect.height
            fish_area = fish.rect.width * fish.rect.height
            
            if player_area > fish_area:
                # Player eats fish
                fish.kill()
                self.grow_player(player)
            else:
                # Fish eats player - Exit for now
                pygame.quit()
                import sys
                sys.exit()

    def grow_player(self, player):
        new_size = player.rect.width + FishSettings.PLAYER_GROWTH_RATE
        center = player.rect.center
        player.image = pygame.Surface((new_size, new_size))
        player.image.fill(ColorSettings.YELLOW)
        player.rect = player.image.get_rect(center=center)