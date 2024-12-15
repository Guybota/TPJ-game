import pygame # type: ignore
from Projectile import Projectile
from sprites import Sprite  # Import the Sprite class
from InputHandler import InputHandler

WIDTH, HEIGHT = 800, 600


# Player class
class Player(Sprite):
    def __init__(self, sprite_path):
        super().__init__(sprite_path, (WIDTH // 2, HEIGHT // 2))

        #Load sprites
        self.idleSprite = self.image.subsurface(pygame.Rect(0, 33, 16, 32))
        self.attackSprite = self.image.subsurface(pygame.Rect(515, 34, 24, 32))
        scale_factor = 2
        self.idleSprite = pygame.transform.scale(self.idleSprite, (self.idleSprite.get_width() * scale_factor, self.idleSprite.get_height() * scale_factor))
        self.attackSprite = pygame.transform.scale(self.attackSprite, (self.attackSprite.get_width() * scale_factor, self.attackSprite.get_height() * scale_factor))

        self.image = self.idleSprite

        self.rect.width = 32 
        self.rect.height = 64  
        
        self.state = "idle"

        self.speed = 5
        self.health = 150
        self.attacking = False
        self.lookingRight = True
        self.attackStartTime = None
        self.attackDuration = 200
        self.hitboxWidth = 70
        self.hitboxHeight = 45
        self.damageDealt = False
        self.hitbox = None 
        self.projectiles = pygame.sprite.Group()

    def update(self, keys_pressed):
        match self.state:
            case "idle":
                input_handler = InputHandler()
                input_handler.handle_input(keys_pressed, self)
                return

            case "attacking":
                if pygame.time.get_ticks() - self.attackStartTime > self.attackDuration:
                    self.hitbox = None
                    self.state = "idle"
                    self.attacking = False
                    self.image = self.idleSprite if self.lookingRight else pygame.transform.flip(self.idleSprite, True, False)
                return

            case "beam":
                # Shoot energy beam
                if keys_pressed[pygame.K_z]: 
                    beam_direction = 1 if self.lookingRight else -1
                    beam_x = self.rect.right if self.lookingRight else self.rect.left - 30
                    beam_y = self.rect.centery
                    projectile = Projectile(beam_x, beam_y, beam_direction, source="player")
                    self.projectiles.add(projectile)
                else:
                    self.state = "idle"
                    self.image = self.idleSprite if self.lookingRight else pygame.transform.flip(self.idleSprite, True, False)
                return
        

    def attack(self, enemy_group):
        if self.attacking and not self.damageDealt:
            # Create a hitbox in front of the player
            if self.lookingRight:
                self.hitbox = pygame.Rect(self.rect.left, self.rect.y, self.hitboxWidth, self.hitboxHeight)
            else:
                self.hitbox = pygame.Rect(self.rect.right - self.hitboxWidth, self.rect.y, self.hitboxWidth, self.hitboxHeight)

            # Check for collision with enemies using the hitbox
            for enemy in enemy_group:
                if self.hitbox.colliderect(enemy.rect):
                    enemy.takeDamage(25)
            
            self.damageDealt = True
        
        # Check if projectiles hit enemies
        for projectile in self.projectiles:
            for enemy in enemy_group:
                if projectile.rect.colliderect(enemy.rect):
                    enemy.takeDamage(10)
                    projectile.kill() 
                    
    def takeDamage(self, amount):
        self.health -= amount