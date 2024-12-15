import pygame # type: ignore
from sprites import Sprite  # Import the Sprite class
import math  # Import math module for calculating distance
from Enemy import Enemy

# Enemy class
class MeleeEnemy(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y)

        self.type = "melee"

        # Load sprites
        self.image = pygame.image.load(r"..\GamePy\Sprites\CellJr.png").convert_alpha()
        self.idleSprite = self.image.subsurface(pygame.Rect(0, 32, 16, 32))  
        self.attackSprite = self.image.subsurface(pygame.Rect(135, 32, 16, 32))  
        scale_factor = 2
        self.idleSprite = pygame.transform.scale(self.idleSprite, (self.idleSprite.get_width() * scale_factor, self.idleSprite.get_height() * scale_factor))
        self.attackSprite = pygame.transform.scale(self.attackSprite, (self.attackSprite.get_width() * scale_factor, self.attackSprite.get_height() * scale_factor))

        # Set initial image and rect
        self.image = self.idleSprite
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self, player):
        match self.attack_in_progress:
            case True:
                if pygame.time.get_ticks() - self.attack_start_time > self.attack_duration:
                    self.image = self.idleSprite
                    self.attack_in_progress = False
                    self.damage_dealt = False
                return
            case False: 
                self.moveToPlayer(player)

                # Attack logic
                if self.rect.colliderect(player.rect) and pygame.time.get_ticks() - self.attack_start_time > 500:  # 500 ms cooldown
                    self.attack(player)
                return
            
    def moveToPlayer(self, player):
        # Calculate movement direction towards player
        dx, dy = 0, 0
        dist = math.hypot(self.rect.x-player.rect.x, self.rect.y-player.rect.y)
        if dist > 30:
            if self.rect.x < player.rect.x:
                dx = self.speed
                self.image = pygame.transform.flip(self.idleSprite, True, False)
            elif self.rect.x > player.rect.x:
                dx = -self.speed
                self.image = self.idleSprite
            if self.rect.y < player.rect.y:
                dy = self.speed
            elif self.rect.y > player.rect.y:
                dy = -self.speed

        # Move enemy
        self.rect.x += dx
        self.rect.y += dy

    def attack(self, player):
        self.attack_start_time = pygame.time.get_ticks()
        self.attack_in_progress = True
        # Attack the player when in range
        if not self.damage_dealt:
            # Create a hitbox for the enemy attack
            attack_hitbox = pygame.Rect(self.rect.centerx - self.attack_width // 2, self.rect.centery - self.attack_height // 2, self.attack_width, self.attack_height)

            # Check if the player is within the attack range
            if attack_hitbox.colliderect(player.rect):
                player.takeDamage(10)  # Dealing damage to the player
                self.damage_dealt = True

            # Switch to attack sprite
            self.image = self.attackSprite