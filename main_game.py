import pygame

# Initialize the game
pygame.init()

# Create the screen
screen = pygame.display.set_mode((800, 600))

# Title and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('image/ufo.png')
pygame.display.set_icon(icon)

# Player
playerX = 400
playerY = 300
playerX_change = 0
playerY_change = 0

class Player:
    def __init__(self, x, y):
        self.image = pygame.image.load('image/player.png')
        self.image = pygame.transform.scale(self.image, (64, 64))
        self.x = x
        self.y = y

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def move(self, x_change, y_change):
        self.x += x_change
        self.y += y_change

# Create player object
player = Player(playerX, playerY)

# Game loop
running = True
while running:
    # Fill the screen with black color
    screen.fill((255, 255, 255))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Check for keystroke events
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -0.3
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.3
            if event.key == pygame.K_UP:
                playerY_change = -0.3
            if event.key == pygame.K_DOWN:
                playerY_change = 0.3

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                playerY_change = 0

    # Move the player
    player.move(playerX_change, playerY_change)

    # Draw the player
    player.draw(screen)

    # Update the display
    pygame.display.update()
