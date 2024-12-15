import pygame # type: ignore
from sprites import Sprite  
from Enemy import Enemy 
from Projectile import Projectile


# Enemy class
class RangedEnemy(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y)

        self.type = "ranged"

        # Load sprites
        self.image = pygame.image.load(r"..\GamePy\Sprites\CellJr2.png").convert_alpha()
        self.idleSprite = self.image.subsurface(pygame.Rect(0, 32, 16, 32)) 
        self.attackSprite = self.image.subsurface(pygame.Rect(135, 32, 16, 32))
        scale_factor = 2
        self.idleSprite = pygame.transform.scale(self.idleSprite, (self.idleSprite.get_width() * scale_factor, self.idleSprite.get_height() * scale_factor))
        self.attackSprite = pygame.transform.scale(self.attackSprite, (self.attackSprite.get_width() * scale_factor, self.attackSprite.get_height() * scale_factor))

        # Set initial image and rect
        self.image = self.idleSprite
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        self.state = "idle"
        self.attack_cooldown = 800

        self.projectiles = pygame.sprite.Group()

    def update(self, player):

        # Check for projectile collisions
        for projectile in self.projectiles:
            if projectile.rect.colliderect(player.rect):
                player.takeDamage(2)
                projectile.kill()

        match self.state:
            case "attacked":
                if pygame.time.get_ticks() - self.attack_start_time > self.attack_cooldown:
                    self.image = self.idleSprite
                    self.state = "idle"
                    self.damage_dealt = False
                return
            case "idle": 
                self.moveToPlayer(player)

                return
            case "attacking":

                self.attack(player)
                return
            
        
            
    def moveToPlayer(self, player):
        # Calculate movement direction towards player
        dx, dy = 0, 0
        xdist = abs(self.rect.x-player.rect.x)
        ydist = abs(self.rect.y-player.rect.y)

        if self.rect.x < player.rect.x:
            self.image = pygame.transform.flip(self.idleSprite, True, False)

        if xdist > 400:
            if self.rect.x < player.rect.x:
                dx = self.speed
            elif self.rect.x > player.rect.x:
                dx = -self.speed
                self.image = self.idleSprite
        elif ydist > 30:
            if self.rect.y < player.rect.y:
                dy = self.speed
            elif self.rect.y > player.rect.y:
                dy = -self.speed   
        else:
            self.attack_start_time = pygame.time.get_ticks()
            self.state = "attacking" 

        # Move enemy
        self.rect.x += dx
        self.rect.y += dy

    def attack(self, player):
        if pygame.time.get_ticks() - self.attack_start_time < self.attack_duration:
            # Spawn a projectile directed toward the player
            direction = 1 if self.rect.x < player.rect.x else -1
            projectile_x = self.rect.right if direction == 1 else self.rect.left - 30
            projectile_y = self.rect.centery
            projectile = Projectile(projectile_x, projectile_y, direction, source="enemy")
            self.projectiles.add(projectile)
        else:
            self.attack_start_time = pygame.time.get_ticks()
            self.state = "attacked"

    def takeDamage(self, amount):
        self.health -= amount
        if self.health <= 0:
            for projectile in self.projectiles:
                projectile.kill()
            self.kill() 