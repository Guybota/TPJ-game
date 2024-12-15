import pygame # type: ignore
import os
import math
import random
from Player import Player
from MeleeEnemy import MeleeEnemy
from RangedEnemy import RangedEnemy
from ScreenSettings import ScreenSettings 

class GameManager():
    def __init__(self):
        # Initialize pygame
        pygame.init()

        # Initialize screen
        self.screenSettings = ScreenSettings()

        # Game settings
        self.FPS = 60
        self.MAX_ENEMIES = 15
        self.ENEMY_MIN_DISTANCE = 100  # Minimum distance from the player for enemy spawn
        self.round_transition_time = None
        # Fonts
        self.font = pygame.font.Font(None, 36)

        # Load the background image
        self.background = pygame.image.load(r"..\GamePy\Sprites\grass.png")

        # Resize the background image to fit the screen size (optional)
        self.background = pygame.transform.scale(self.background, (self.screenSettings.WIDTH, self.screenSettings.HEIGHT))

        # Initialize player with the path to the sprite sheet
        self.player = Player(r"..\GamePy\Sprites\Goku_spr.png")
        self.allSprites = pygame.sprite.Group(self.player)

        # Initialize first enemy wave
        self.roundCount = 1
        self.enemyGroup = self.spawn_enemies(self.roundCount, self.player)

        self.highscore = self.load_highscore()

        # Sprite groups
        self.allSprites = pygame.sprite.Group()
        self.allSprites.add(self.player)
        self.allSprites.add(self.enemyGroup)    

    def check_enemy_count(self):
        if len(self.enemyGroup) == 0:
            if self.round_transition_time is None:
                self.round_transition_time = pygame.time.get_ticks()  # Start delay timer
            
            # After 2 seconds, spawn new enemies for the next round
            if pygame.time.get_ticks() - self.round_transition_time > 2000:
                self.roundCount += 1
                self.enemyGroup = self.spawn_enemies(min(self.roundCount, self.MAX_ENEMIES), self.player)
                self.allSprites.add(self.enemyGroup)
                self.round_transition_time = None

    def spawn_enemies(self, numEnemies, player):
        enemies = pygame.sprite.Group()
        meleeNum = math.ceil(numEnemies * 0.55)
        for i in range(numEnemies):
            while True:
                x, y = random.randint(50, self.screenSettings.WIDTH - 50), random.randint(50, self.screenSettings.HEIGHT - 50)
                # Ensure enemy spawns at a minimum distance from the player
                if abs(x - player.rect.x) > self.ENEMY_MIN_DISTANCE and abs(y - player.rect.y) > self.ENEMY_MIN_DISTANCE:
                    break
            
            enemy = MeleeEnemy(x, y) if i <= meleeNum else RangedEnemy(x, y)
            enemies.add(enemy)
        return enemies
    
    def draw_ui(self):
        # Display player health
            pygame.draw.rect(self.screenSettings.screen, self.screenSettings.BLACK, (5, 5, 160, 30))
            pygame.draw.rect(self.screenSettings.screen, self.screenSettings.RED, (10, 10, 150, 20))
            pygame.draw.rect(self.screenSettings.screen, self.screenSettings.GREEN, (10, 10, self.player.health, 20))

            # Display round counter at the top center
            roundText = self.font.render(f"Round {self.roundCount}", True, self.screenSettings.WHITE)
            roundTextBorder = self.font.render(f"Round {self.roundCount}", True, self.screenSettings.BLACK)
            # Draw borders
            self.screenSettings.screen.blit(roundTextBorder, ((self.screenSettings.WIDTH // 2 - roundText.get_width() // 2) + 2, 10))
            self.screenSettings.screen.blit(roundTextBorder, ((self.screenSettings.WIDTH // 2 - roundText.get_width() // 2)- 2, 10))
            self.screenSettings.screen.blit(roundTextBorder, (self.screenSettings.WIDTH // 2 - roundText.get_width() // 2, 12))
            self.screenSettings.screen.blit(roundTextBorder, (self.screenSettings.WIDTH // 2 - roundText.get_width() // 2, 8))

            self.screenSettings.screen.blit(roundText, (self.screenSettings.WIDTH // 2 - roundText.get_width() // 2, 10))

    def game_over_screen(self):
        pygame.draw.rect(self.screenSettings.screen, self.screenSettings.BLACK, (0, 0, self.screenSettings.WIDTH, self.screenSettings.HEIGHT))
        overText1 = self.font.render("Game over", True, self.screenSettings.WHITE)
        overText2 = self.font.render(f"Round {self.roundCount}", True, self.screenSettings.WHITE)
        overText3 = self.font.render(f"Highscore: {self.highscore}", True, self.screenSettings.WHITE)
        overText4 = self.font.render("Press 'R' to restart or Press 'Esc' to quit", True, self.screenSettings.WHITE)
        self.screenSettings.screen.blit(overText1, (self.screenSettings.WIDTH // 2 - overText1.get_width() // 2, (self.screenSettings.HEIGHT // 2 - overText3.get_height() // 2) - 75))
        self.screenSettings.screen.blit(overText2, (self.screenSettings.WIDTH // 2 - overText2.get_width() // 2, (self.screenSettings.HEIGHT // 2 - overText3.get_height() // 2) -30))
        self.screenSettings.screen.blit(overText3, (self.screenSettings.WIDTH // 2 - overText3.get_width() // 2, self.screenSettings.HEIGHT // 2 - overText3.get_height() // 2))
        self.screenSettings.screen.blit(overText4, (self.screenSettings.WIDTH // 2 - overText4.get_width() // 2, (self.screenSettings.HEIGHT // 2 - overText3.get_height() // 2) + 30))

    
    def load_highscore(self):
        # Check if the file exists
        if os.path.exists("highscore.txt"):
            with open("highscore.txt", "r") as file:
                try:
                    return int(file.read())  # Read and return the highscore as an integer
                except ValueError:
                    return 0  # If file content is invalid, return 0 as the default highscore
        else:
            return 0  # If the file doesn't exist, return 0 as the default highscore
        
    def save_highscore(self):
        with open("highscore.txt", "w") as file:
            file.write(str(self.highscore))  # Write the highscore as a string

    def update_highscore(self):
        if self.roundCount > self.highscore:
            self.highscore = self.roundCount  
            self.save_highscore()  # Save the new highscore to the file


    