import pygame # type: ignore
import Commands

class InputHandler:
    def __init__(self):
        self.command_map = {
            pygame.K_UP: Commands.MoveUp(),
            pygame.K_w: Commands.MoveUp(),
            pygame.K_DOWN: Commands.MoveDown(),
            pygame.K_s: Commands.MoveDown(),
            pygame.K_LEFT: Commands.MoveLeft(),
            pygame.K_a: Commands.MoveLeft(),
            pygame.K_RIGHT: Commands.MoveRight(),
            pygame.K_d: Commands.MoveRight(),
            pygame.K_SPACE: Commands.Attack(),
            pygame.K_z: Commands.ShootProjectile(),
        }

    def handle_input(self, keys_pressed, player):
        for key, command in self.command_map.items():
            if keys_pressed[key]:
                command.execute(player)