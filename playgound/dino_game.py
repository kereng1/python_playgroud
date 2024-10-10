import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 400
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chrome Dino Game")

# Clock to control the frame rate
clock = pygame.time.Clock()

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GROUND_HEIGHT = HEIGHT - 70

# Dinosaur settings
dino_width, dino_height = 50, 50
dino_x = 50
dino_y = GROUND_HEIGHT - dino_height
dino_velocity = 0
gravity = 1
is_jumping = False

# Obstacle settings
obstacle_width, obstacle_height = 20, 50
obstacle_x = WIDTH
obstacle_y = GROUND_HEIGHT - obstacle_height
obstacle_velocity = 7

# Game variables
score = 0
font = pygame.font.SysFont(None, 36)

def draw_dino(x, y):
    pygame.draw.rect(SCREEN, BLACK, (x, y, dino_width, dino_height))

def draw_obstacle(x, y):
    pygame.draw.rect(SCREEN, (200, 0, 0), (x, y, obstacle_width, obstacle_height))

def show_score(current_score):
    score_text = font.render(f"Score: {current_score}", True, BLACK)
    SCREEN.blit(score_text, (10, 10))

def game_over_screen():
    # Display Game Over message
    SCREEN.fill(WHITE)
    game_over_text = font.render("Game Over!", True, BLACK)
    restart_text = font.render("Press R to Restart or Q to Quit", True, BLACK)
    SCREEN.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 50))
    SCREEN.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2))
    pygame.display.update()

    waiting = True
    while waiting:
        clock.tick(15)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    waiting = False
                    main()  # Restart the game
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

def main():
    global dino_y, dino_velocity, is_jumping, obstacle_x, score

    # Reset game variables
    dino_y = GROUND_HEIGHT - dino_height
    dino_velocity = 0
    is_jumping = False
    obstacle_x = WIDTH
    score = 0

    running = True
    while running:
        clock.tick(60)
        SCREEN.fill(WHITE)
        pygame.draw.line(SCREEN, BLACK, (0, GROUND_HEIGHT), (WIDTH, GROUND_HEIGHT), 2)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

            # Jumping mechanism
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not is_jumping:
                    dino_velocity = -15
                    is_jumping = True

        # Apply gravity
        if is_jumping:
            dino_velocity += gravity
            dino_y += dino_velocity

            if dino_y >= GROUND_HEIGHT - dino_height:
                dino_y = GROUND_HEIGHT - dino_height
                is_jumping = False

        # Move obstacle
        obstacle_x -= obstacle_velocity
        if obstacle_x < -obstacle_width:
            obstacle_x = WIDTH + random.randint(0, 100)
            score += 1  # Increase score when obstacle passes

        # Collision detection
        dino_rect = pygame.Rect(dino_x, dino_y, dino_width, dino_height)
        obstacle_rect = pygame.Rect(obstacle_x, obstacle_y, obstacle_width, obstacle_height)

        if dino_rect.colliderect(obstacle_rect):
            game_over_screen()
            return  # Exit the main function to prevent further updates

        # Draw elements
        draw_dino(dino_x, dino_y)
        draw_obstacle(obstacle_x, obstacle_y)
        show_score(score)

        pygame.display.update()

if __name__ == "__main__":
    main()
