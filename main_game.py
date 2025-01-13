import pygame
import math
import random
import time

# Initialize the game
pygame.init()

# Create the screen
screen = pygame.display.set_mode((800, 600))

# Title and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('image/ufo.png')
pygame.display.set_icon(icon)

# Load images
heart_image = pygame.image.load('image/heart.png')
heart_image = pygame.transform.scale(heart_image, (32, 32))

# Load custom font
custom_font = pygame.font.Font('fonts/Jersey10-Regular.ttf', 74)
custom_font_small = pygame.font.Font('fonts/Jersey10-Regular.ttf', 36)
enemy_font = pygame.font.Font('fonts/Jersey10-Regular.ttf', 27)

# Game state
game_started = False
game_over = False
player_failed = False

# Bullet class
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction_x, direction_y, speed=3):
        super().__init__()
        self.image = pygame.Surface((10, 10))
        self.image.fill((255, 0, 0))  # Red bullet
        self.rect = self.image.get_rect(center=(x, y))
        magnitude = math.sqrt(direction_x**2 + direction_y**2)
        self.speed_x = (direction_x / magnitude) * speed
        self.speed_y = (direction_y / magnitude) * speed

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        if self.rect.right < 0 or self.rect.left > 800 or self.rect.bottom < 0 or self.rect.top > 600:
            self.kill()

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, lives):
        super().__init__()
        self.image_right = pygame.image.load('image/player.png').convert_alpha()
        self.image_right = pygame.transform.scale(self.image_right, (64, 64))
        self.image_left = pygame.transform.flip(self.image_right, True, False)
        self.image = self.image_right
        self.rect = self.image.get_rect(topleft=(x, y))
        self.lives = lives

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)

    def move(self, x_change, y_change):
        self.rect.x += x_change
        self.rect.y += y_change
        self.check_borders()

    def check_borders(self):
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > 800:
            self.rect.right = 800
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > 600:
            self.rect.bottom = 600

    def player_hit(self):
        if self.lives > 0:
            self.lives -= 1
        return self.lives > 0

    def draw_lives(self, screen):
        for i in range(self.lives):
            screen.blit(heart_image, (10 + i * 40, 10))

    def update_direction(self, mouse_x):
        if mouse_x < self.rect.centerx:
            self.image = self.image_left
        else:
            self.image = self.image_right

# Enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, max_health):
        super().__init__()
        self.image = pygame.image.load('image/enemy.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (90, 90))  # Adjusted size
        self.rect = self.image.get_rect(topleft=(x, y))
        self.max_health = max_health
        self.current_health = max_health
        self.last_shot = 0  # Time of the last shot
        self.direction_x = random.choice([-1, 1])
        self.direction_y = random.choice([-1, 1])
        self.speed = 0.6

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)

    def draw_health_bar(self, screen, x, y, label):
        bar_width = 150
        bar_height = 10
        health_ratio = self.current_health / self.max_health
        health_bar_width = int(bar_width * health_ratio)
        label_text = enemy_font.render(label, True, (0, 0, 0))
        screen.blit(label_text, (x - 80, y - 5))
        pygame.draw.rect(screen, (255, 0, 0), (x, y, bar_width, bar_height))
        pygame.draw.rect(screen, (0, 255, 0), (x, y, health_bar_width, bar_height))

    def shoot(self, bullets):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot > 1000:  # Fire every 1 second
            self.last_shot = current_time
            angles = [0, 60, 120, 180, 240, 300]
            for angle in angles:
                direction_x = math.cos(math.radians(angle))
                direction_y = math.sin(math.radians(angle))
                bullet = Bullet(self.rect.centerx, self.rect.centery, direction_x, direction_y, speed=2)
                bullets.add(bullet)

    def move(self):
        self.rect.x += self.direction_x * self.speed
        self.rect.y += self.direction_y * self.speed
        self.check_borders()

        # Change direction randomly
        if random.randint(1, 100) == 1:
            self.direction_x = random.choice([-1, 1])
            self.direction_y = random.choice([-1, 1])

    def check_borders(self):
        if self.rect.left < 0 or self.rect.right > 800:
            self.direction_x *= -1
        if self.rect.top < 0 or self.rect.bottom > 600:
            self.direction_y *= -1

# Initialize player and enemies
player = Player(100, 300, 3)  # Updated player position
enemy1 = Enemy(500, 200, max_health=100)  # First enemy
enemy2 = Enemy(300, 100, max_health=100)  # Second enemy

# Bullet groups
player_bullets = pygame.sprite.Group()
enemy_bullets = pygame.sprite.Group()

# Enemy group
enemies = pygame.sprite.Group()
enemies.add(enemy1)
enemies.add(enemy2)

# Movement variables
x_change = 0
y_change = 0
speed = 1  # Movement speed

# Function to display the start screen
def show_start_screen():
    screen.fill((255, 255, 255))  # White background
    title_text = custom_font.render("Space Invaders", True, (0, 0, 0))
    start_text = custom_font_small.render("Press Start to Begin", True, (0, 0, 0))
    screen.blit(title_text, (200, 200))
    screen.blit(start_text, (260, 300))

    # Draw start button
    start_button = pygame.Rect(350, 400, 100, 50)
    pygame.draw.rect(screen, (0, 255, 0), start_button)
    button_text = custom_font_small.render("Start", True, (0, 0, 0))
    screen.blit(button_text, (start_button.x + 19, start_button.y + 5))

    pygame.display.update()
    return start_button

# Function to display the game over screen
def show_game_over_screen(message):
    screen.fill((255, 255, 255))  # White background
    game_over_text = custom_font.render(message, True, (0, 0, 0))
    screen.blit(game_over_text, (200, 200))

    # Draw play again button
    play_again_button = pygame.Rect(250, 400, 150, 50)
    pygame.draw.rect(screen, (0, 255, 0), play_again_button)
    play_again_text = custom_font_small.render("Play Again", True, (0, 0, 0))
    screen.blit(play_again_text, (play_again_button.x + 15, play_again_button.y + 5))

    # Draw exit button
    exit_button = pygame.Rect(450, 400, 100, 50)
    pygame.draw.rect(screen, (255, 0, 0), exit_button)
    exit_text = custom_font_small.render("Exit", True, (0, 0, 0))
    screen.blit(exit_text, (exit_button.x + 30, exit_button.y + 5))

    pygame.display.update()
    return play_again_button, exit_button

# Function to display the countdown
def show_countdown():
    for i in range(3, 0, -1):
        screen.fill((255, 255, 255))  # White background
        countdown_text = custom_font.render(str(i), True, (0, 0, 0))
        screen.blit(countdown_text, (screen.get_width() // 2 - countdown_text.get_width() // 2, screen.get_height() // 2 - countdown_text.get_height() // 2))
        pygame.display.update()
        time.sleep(1)

# Game loop
running = True
while running:
    if not game_started:
        start_button = show_start_screen()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(event.pos):
                    show_countdown()
                    game_started = True
    elif game_over or player_failed:
        message = "Enemy defeated!" if game_over else "    You Failed"
        play_again_button, exit_button = show_game_over_screen(message)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_again_button.collidepoint(event.pos):
                    # Reset game state
                    show_countdown()
                    game_started = True
                    game_over = False
                    player_failed = False
                    player = Player(100, 300, 3)
                    enemy1 = Enemy(500, 200, max_health=100)
                    enemy2 = Enemy(300, 100, max_health=100)
                    player_bullets.empty()
                    enemy_bullets.empty()
                    enemies.empty()
                    enemies.add(enemy1)
                    enemies.add(enemy2)
                if exit_button.collidepoint(event.pos):
                    running = False
    else:
        screen.fill((255, 255, 255))  # White background

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Key pressed
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    x_change = -speed
                if event.key == pygame.K_d:
                    x_change = speed
                if event.key == pygame.K_w:
                    y_change = -speed
                if event.key == pygame.K_s:
                    y_change = speed

            # Key released
            if event.type == pygame.KEYUP:
                if event.key in [pygame.K_a, pygame.K_d]:
                    x_change = 0
                if event.key in [pygame.K_w, pygame.K_s]:
                    y_change = 0

            # Mouse click to shoot
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                target_x, target_y = event.pos
                direction_x = target_x - player.rect.centerx
                direction_y = target_y - player.rect.centery
                bullet = Bullet(player.rect.centerx, player.rect.centery, direction_x, direction_y)
                player_bullets.add(bullet)

        # Update player position
        player.move(x_change, y_change)

        # Update player direction based on mouse position
        mouse_x, _ = pygame.mouse.get_pos()
        player.update_direction(mouse_x)

        # Update bullets
        player_bullets.update()
        enemy_bullets.update()

        # Enemy movement and shooting
        for enemy in enemies:
            enemy.move()
            enemy.shoot(enemy_bullets)

        # Collision detection
        for bullet in player_bullets:
            for enemy in enemies:
                if bullet.rect.colliderect(enemy.rect):
                    bullet.kill()
                    enemy.current_health -= 10
                    if enemy.current_health <= 0:
                        enemies.remove(enemy)
                        if len(enemies) == 0:
                            game_over = True

        for bullet in enemy_bullets:
            if bullet.rect.colliderect(player.rect):
                bullet.kill()
                if not player.player_hit():
                    player_failed = True

        # Draw everything
        player.draw(screen)
        player.draw_lives(screen)
        enemies.draw(screen)
        player_bullets.draw(screen)
        enemy_bullets.draw(screen)

        # Draw enemy health bars
        if enemy1.current_health > 0:
            enemy1.draw_health_bar(screen, 600, 10, "Enemy1")
        if enemy2.current_health > 0:
            enemy2.draw_health_bar(screen, 600, 30, "Enemy2")

        pygame.display.update()
