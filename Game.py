import pygame # type: ignore
from GameManager import GameManager


gameManager = GameManager()

# Game loop
clock = pygame.time.Clock()
running = True
state = "running"

while running:
    clock.tick(gameManager.FPS)
    
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    match state:
        case "running":
            # Key handling
            keysPressed = pygame.key.get_pressed()
            gameManager.player.update(keysPressed)

            # Player attacks
            gameManager.player.attack(gameManager.enemyGroup)

            # Update enemies
            gameManager.enemyGroup.update(gameManager.player)

            gameManager.player.projectiles.update(gameManager.screenSettings.WIDTH)
            for enemy in gameManager.enemyGroup:
                if enemy.type == "ranged":
                    enemy.projectiles.update(gameManager.screenSettings.WIDTH)

            # Check if player is defeated
            if gameManager.player.health <= 0:
                gameManager.update_highscore()
                state = "over"

            # Check if all enemies are defeated
            gameManager.check_enemy_count()

            gameManager.allSprites.add(gameManager.player.projectiles)

            for enemy in gameManager.enemyGroup:
                if enemy.type == "ranged":
                    gameManager.allSprites.add(enemy.projectiles)

            # Draw the background
            gameManager.screenSettings.screen.blit(gameManager.background, (0, 0))

            # Draw everything else
            gameManager.allSprites.draw(gameManager.screenSettings.screen)

            gameManager.draw_ui()
 
        case "over":
            keysPressed = pygame.key.get_pressed()
            if keysPressed[pygame.K_r]:
                gameManager = GameManager()
                state = "running"
            elif keysPressed[pygame.K_ESCAPE]:
                running = False

            gameManager.game_over_screen()
            

    # Update display
    pygame.display.flip()

pygame.quit()
