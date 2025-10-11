import pygame
import sys
import random
import math

# --- Constants ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GRID_SIZE = 20
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (220, 50, 50)
GREEN = (50, 220, 50)
BLUE = (50, 50, 220)
PURPLE = (160, 32, 240)
PLAYER_COLOR = (0, 200, 200)

# Player settings
PLAYER_SPEED = 8
PLAYER_AREA_HEIGHT = 100 # How far up the player can move

# Millipede settings
MILLIPEDE_SPEED = 2

# --- Game Classes ---

class Player(pygame.sprite.Sprite):
    """ Represents the player's ship. """
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([GRID_SIZE, GRID_SIZE])
        self.image.fill(PLAYER_COLOR)
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.bottom = SCREEN_HEIGHT - 10
        self.speed_x = 0

    def update(self):
        """ Update player position based on speed. """
        self.rect.x += self.speed_x
        # Prevent player from moving off-screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top < SCREEN_HEIGHT - PLAYER_AREA_HEIGHT:
            self.rect.top = SCREEN_HEIGHT - PLAYER_AREA_HEIGHT
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

    def shoot(self):
        """ Creates a new bullet instance. """
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)

class Bullet(pygame.sprite.Sprite):
    """ Represents a bullet fired by the player. """
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface([GRID_SIZE // 4, GRID_SIZE // 2])
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed_y = -12

    def update(self):
        """ Move the bullet up the screen. """
        self.rect.y += self.speed_y
        # Kill the bullet if it goes off the top of the screen
        if self.rect.bottom < 0:
            self.kill()

class Mushroom(pygame.sprite.Sprite):
    """ Represents a mushroom obstacle. """
    def __init__(self, center_pos):
        super().__init__()
        self.image = pygame.Surface([GRID_SIZE, GRID_SIZE])
        self.health = 4
        self.update_color()
        self.rect = self.image.get_rect()
        self.rect.center = center_pos

    def take_damage(self):
        """ Reduces mushroom health and updates its color. """
        self.health -= 1
        if self.health <= 0:
            self.kill()
        else:
            self.update_color()

    def update_color(self):
        """ Changes color based on health. """
        color_value = 255 - (4 - self.health) * 60
        self.image.fill((color_value, 0, color_value))

class MillipedeSegment(pygame.sprite.Sprite):
    """ A single segment of the millipede. """
    def __init__(self, x, y, is_head=False):
        super().__init__()
        self.image = pygame.Surface([GRID_SIZE, GRID_SIZE], pygame.SRCALPHA)
        color = RED if is_head else GREEN
        pygame.draw.circle(self.image, color, (GRID_SIZE // 2, GRID_SIZE // 2), GRID_SIZE // 2)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.vx = MILLIPEDE_SPEED
        self.vy = 0
        self.is_head = is_head

    def update_head_color(self):
        """ Updates the segment to look like a head. """
        self.is_head = True
        pygame.draw.circle(self.image, RED, (GRID_SIZE // 2, GRID_SIZE // 2), GRID_SIZE // 2)


# --- Main Game Setup ---
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Loapede")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

# Sprite Groups
all_sprites = pygame.sprite.Group()
mushrooms = pygame.sprite.Group()
bullets = pygame.sprite.Group()
millipede_segments = pygame.sprite.Group()

# Game Variables
score = 0
lives = 3
game_over = False

def create_mushroom_field():
    """ Creates a random field of mushrooms at the start of the game. """
    for _ in range(40):
        x = random.randrange(0, SCREEN_WIDTH // GRID_SIZE) * GRID_SIZE
        y = random.randrange(1, (SCREEN_HEIGHT - PLAYER_AREA_HEIGHT) // GRID_SIZE) * GRID_SIZE
        # Avoid placing mushrooms too close to each other initially
        if not any(m.rect.center == (x + GRID_SIZE // 2, y + GRID_SIZE // 2) for m in mushrooms):
            mushroom = Mushroom((x + GRID_SIZE // 2, y + GRID_SIZE // 2))
            all_sprites.add(mushroom)
            mushrooms.add(mushroom)

def create_millipede(length):
    """ Creates a millipede train. """
    train = []
    start_x = SCREEN_WIDTH // 2
    for i in range(length):
        is_head = (i == 0)
        # Segments are initially placed off-screen to the left to "crawl in"
        segment = MillipedeSegment(start_x - i * GRID_SIZE, 0, is_head)
        train.append(segment)
        all_sprites.add(segment)
        millipede_segments.add(segment)
    return [train] # Return a list containing the single train

def show_game_over_screen():
    """ Displays the game over message. """
    text = font.render("GAME OVER", True, WHITE)
    text_rect = text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 50))
    score_text = font.render(f"Final Score: {score}", True, WHITE)
    score_rect = score_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
    restart_text = font.render("Press 'R' to Restart", True, WHITE)
    restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 50))
    
    screen.blit(text, text_rect)
    screen.blit(score_text, score_rect)
    screen.blit(restart_text, restart_rect)
    pygame.display.flip()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                waiting = False

def reset_game():
    """ Resets all game variables to their initial state. """
    global score, lives, game_over, millipede_trains
    
    # Clear all sprites except the player
    for sprite in all_sprites:
        sprite.kill()
        
    score = 0
    lives = 3
    game_over = False
    
    # Re-create game objects
    global player
    player = Player()
    all_sprites.add(player)
    
    create_mushroom_field()
    millipede_trains = create_millipede(12)


# --- Game Initialization ---
player = Player()
all_sprites.add(player)
create_mushroom_field()
millipede_trains = create_millipede(12)

# --- Game Loop ---
running = True
while running:
    if game_over:
        show_game_over_screen()
        reset_game()

    # 1. Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if not game_over:
                if event.key == pygame.K_LEFT:
                    player.speed_x = -PLAYER_SPEED
                if event.key == pygame.K_RIGHT:
                    player.speed_x = PLAYER_SPEED
                if event.key == pygame.K_SPACE:
                    player.shoot()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT and player.speed_x < 0:
                player.speed_x = 0
            if event.key == pygame.K_RIGHT and player.speed_x > 0:
                player.speed_x = 0

    # 2. Update
    if not game_over:
        all_sprites.update()

        # Millipede Logic
        new_trains = []
        for train in millipede_trains:
            if not train: continue
            
            head = train[0]
            old_head_pos = head.rect.copy()

            # Move head
            head.rect.x += head.vx
            
            # Head collision detection (screen bounds and mushrooms)
            hit_obstacle = False
            if head.rect.left < 0 or head.rect.right > SCREEN_WIDTH:
                hit_obstacle = True
            
            collided_mushrooms = pygame.sprite.spritecollide(head, mushrooms, False)
            if collided_mushrooms:
                hit_obstacle = True
                # Nudge the head back to avoid getting stuck inside mushroom
                head.rect.x -= head.vx

            if hit_obstacle:
                head.vx *= -1
                head.rect.x += head.vx # Move one step in new direction
                head.rect.y += GRID_SIZE
                # If millipede reaches player area, it moves back and forth there
                if head.rect.bottom > SCREEN_HEIGHT:
                    head.rect.bottom = SCREEN_HEIGHT

            # Update body segments
            # Each segment moves to the previous position of the one in front
            prev_pos = old_head_pos
            for segment in train[1:]:
                current_pos = segment.rect.copy()
                segment.rect.topleft = prev_pos.topleft
                prev_pos = current_pos

        # Bullet-Mushroom Collisions
        hits = pygame.sprite.groupcollide(bullets, mushrooms, True, False)
        for bullet, mushroom_list in hits.items():
            for mushroom in mushroom_list:
                mushroom.take_damage()
                score += 1

        # Bullet-Millipede Collisions
        hits = pygame.sprite.groupcollide(bullets, millipede_segments, True, True)
        for bullet, segments_hit in hits.items():
            for segment in segments_hit:
                score += 10
                # Create a mushroom where segment was hit
                mushroom = Mushroom(segment.rect.center)
                all_sprites.add(mushroom)
                mushrooms.add(mushroom)

                # Find which train and position the segment was in
                for train in millipede_trains:
                    if segment in train:
                        idx = train.index(segment)
                        # If a middle segment is hit, split the train
                        if 0 < idx < len(train) - 1:
                            new_train = train[idx+1:]
                            # The segment after the destroyed one becomes a new head
                            if new_train:
                                new_train[0].update_head_color()
                                new_trains.append(new_train)
                            # Truncate the original train
                            millipede_trains[millipede_trains.index(train)] = train[:idx]
                        break
            millipede_trains.extend(new_trains)
            new_trains.clear()


        # Millipede-Player Collision
        hits = pygame.sprite.spritecollide(player, millipede_segments, True)
        if hits:
            lives -= 1
            if lives <= 0:
                game_over = True
            # Simple "respawn" by recreating the player
            player.kill()
            player = Player()
            all_sprites.add(player)


    # 3. Draw / Render
    screen.fill(BLACK)
    all_sprites.draw(screen)

    # Draw Score and Lives
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))
    lives_text = font.render(f"Lives: {lives}", True, WHITE)
    screen.blit(lives_text, (SCREEN_WIDTH - 120, 10))

    pygame.display.flip()

    # 4. Maintain frame rate
    clock.tick(FPS)

pygame.quit()
sys.exit()

