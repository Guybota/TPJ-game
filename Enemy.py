import pygame # type: ignore
from sprites import Sprite  # Import the Sprite class

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        self.type = ""
        # Load sprite sheet and extract idle and attack sprites
        self.image = pygame.image.load(r"..\GamePy\Sprites\CellJr.png").convert_alpha()
        self.idleSprite = self.image.subsurface(pygame.Rect(0, 32, 16, 32))  
        self.attackSprite = self.image.subsurface(pygame.Rect(135, 32, 16, 32))  

        # Scale the sprites (double the size)
        scale_factor = 2
        self.idleSprite = pygame.transform.scale(self.idleSprite, (self.idleSprite.get_width() * scale_factor, self.idleSprite.get_height() * scale_factor))
        self.attackSprite = pygame.transform.scale(self.attackSprite, (self.attackSprite.get_width() * scale_factor, self.attackSprite.get_height() * scale_factor))

        # Set initial image and rect
        self.image = self.idleSprite
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        self.health = 50
        self.speed = 2
        self.last_attack_time = 0  # To track attack cooldown

        # Attack hitbox properties
        self.attack_width = 60
        self.attack_height = 40
        self.attack_range = 50
        self.attack_start_time = 0
        self.attack_duration = 100  # Attack for 100ms
        self.damage_dealt = False
        self.attack_in_progress = False


    def takeDamage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.kill()  # Remove the enemy if health is depleted

