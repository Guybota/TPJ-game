import pygame # type: ignore

class Command:
    def execute(self, player):
        raise NotImplementedError

class MoveUp(Command):
    def execute(self, player):
        if player.state == "idle":
            player.rect.y -= player.speed

class MoveDown(Command):
    def execute(self, player):
        if player.state == "idle":
            player.rect.y += player.speed

class MoveLeft(Command):
    def execute(self, player):
        if player.state == "idle":
            player.rect.x -= player.speed
            player.lookingRight = False
            player.image = pygame.transform.flip(player.idleSprite, True, False)

class MoveRight(Command):
    def execute(self, player):
        if player.state == "idle":
            player.rect.x += player.speed
            player.lookingRight = True
            player.image = player.idleSprite

class Attack(Command):
    def execute(self, player):
        if player.state == "idle":
            player.attackStartTime = pygame.time.get_ticks()
            player.damageDealt = False
            player.attacking = True
            player.state = "attacking"
            if player.lookingRight:
                player.image = player.attackSprite
            else: 
                player.image = pygame.transform.flip(player.attackSprite, True, False)

class ShootProjectile(Command):
    def execute(self, player):
        if player.state == "idle":
            player.state = "beam"
            player.image = player.attackSprite if player.lookingRight else pygame.transform.flip(player.attackSprite, True, False)