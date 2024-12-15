import pygame # type: ignore

class ScreenSettings():
    def __init__(self):

        # Screen dimensions
        self.WIDTH, self.HEIGHT = 900, 700
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Kogu's Gauntlet")

        # Colors
        self.WHITE = (255, 255, 255)
        self.RED = (255, 0, 0)
        self.GREEN = (0, 255, 0)
        self.BLACK = (0, 0, 0)

        # Fonts
        self.font = pygame.font.Font(None, 36)

        # Load the background image
        self.background = pygame.image.load(r"..\GamePy\Sprites\grass.png")

        # Resize the background image to fit the screen size (optional)
        self.background = pygame.transform.scale(self.background, (self.WIDTH, self.HEIGHT))