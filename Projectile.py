import pygame # type: ignore

class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, source, speed=10):
        super().__init__()
        self.source = source
        self.image = pygame.Surface((30, 10)) # Beam size
        self.image.fill((255, 0, 0) if source == "enemy" else (255, 255, 0))  # Red for enemy, yellow for player
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.direction = direction
        self.speed = speed

    def update(self, screenWidth):
        self.rect.x += self.speed * self.direction

        # Remove the projectile if it goes off-screen
        if self.rect.right < 0 or self.rect.left > screenWidth:
            self.kill()
