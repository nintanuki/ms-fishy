import pygame
import random
from core.sprites import Fish
from settings import FishSettings, ColorSettings, PlayerSettings

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

        # random.random() gives 0.0 to 1.0. 
        # Squaring it (or cubing it) makes small numbers much more common.
        skew_factor = random.random()**32  # Higher exponent = more small fish
        size_range = FishSettings.MAX_SIZE - FishSettings.MIN_SIZE
        size = int(FishSettings.MIN_SIZE + (skew_factor * size_range))

        # Calculate speed (Inversely proportional to size)
        size_range = FishSettings.MAX_SIZE - FishSettings.MIN_SIZE
        # We use a 0.0 to 1.0 ratio of where this fish sits in the size range
        size_ratio = (size - FishSettings.MIN_SIZE) / size_range

        speed_range = FishSettings.MAX_SPEED - FishSettings.MIN_SPEED
        # 1.0 ratio (big fish) -> Min Speed | 0.0 ratio (small fish) -> Max Speed
        speed = FishSettings.MAX_SPEED - (size_ratio * speed_range)
        
        new_fish = Fish(side, size, speed)
        self.sprite_group.add(new_fish)

    def check_collisions(self, player):
        # We use pygame.sprite.spritecollide with a custom callback or manual loop
        # We pass False for dokill because we want to decide which one gets removed (player or fish) based on their relative sizes.
        collided_fish = pygame.sprite.spritecollide(player, self.sprite_group, False, pygame.sprite.collide_mask)
        
        # If there are multiple collisions in the same frame, we process them one at a time.
        for fish in collided_fish:
            # Compare areas to determine if the player eats the fish or vice versa.
            player_area = player.rect.width * player.rect.height
            fish_area = fish.size * fish.size
            
            # If the player's area is larger than the fish's area, the player eats the fish.
            if player_area > fish_area:
                # Player eats fish
                fish.kill()
                self.grow_player(player, fish)
            else:
                # Fish eats player - Exit for now
                pygame.quit()
                import sys
                sys.exit()

    def grow_player(self, player, fish):
        growth_amount = fish.size * PlayerSettings.PLAYER_GROWTH_COEFFICIENT
        
        new_size = int(player.rect.width + growth_amount)
        
        # Keep the player centered so they don't "jump" when growing
        center = player.rect.center
        player.image = pygame.Surface((new_size, new_size))
        player.image.fill(ColorSettings.YELLOW)
        player.rect = player.image.get_rect(center=center)
        # Rebuild the mask to match the new surface size after growing.
        player.mask = pygame.mask.from_surface(player.image)