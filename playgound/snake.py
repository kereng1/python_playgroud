import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480

# Grid size
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Game states
STATE_MAIN_MENU = 'main_menu'
STATE_PLAYING = 'playing'
STATE_GAME_OVER = 'game_over'

# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()

# Fonts
font_small = pygame.font.SysFont("Arial", 20)
font_large = pygame.font.SysFont("Arial", 40)

# Helper functions
def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect(center=(x, y))
    surface.blit(textobj, textrect)

# Classes
class SnakeSegment(pygame.sprite.Sprite):
    def __init__(self, position, color):
        super().__init__()
        self.image = pygame.Surface((GRID_SIZE, GRID_SIZE))
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft=position)

class Snake:
    def __init__(self, color, start_pos):
        self.color = color
        self.segments = []
        self.direction = pygame.K_RIGHT
        self.positions = [start_pos]
        head = SnakeSegment(self.positions[0], self.color)
        self.segments.append(head)
        self.growing = False

    def move(self):
        x, y = self.positions[0]
        if self.direction == pygame.K_UP:
            y -= GRID_SIZE
        elif self.direction == pygame.K_DOWN:
            y += GRID_SIZE
        elif self.direction == pygame.K_LEFT:
            x -= GRID_SIZE
        elif self.direction == pygame.K_RIGHT:
            x += GRID_SIZE
        new_head_pos = (x % SCREEN_WIDTH, y % SCREEN_HEIGHT)
        self.positions.insert(0, new_head_pos)
        if not self.growing:
            self.positions.pop()
            self.segments.pop()
        else:
            self.growing = False
        new_head_segment = SnakeSegment(new_head_pos, self.color)
        self.segments.insert(0, new_head_segment)

    def grow(self):
        self.growing = True

    def check_collision(self):
        # Check for collision with self
        if self.positions[0] in self.positions[1:]:
            return True
        return False

    @property
    def head_rect(self):
        return self.segments[0].rect

class Food(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((GRID_SIZE, GRID_SIZE))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.spawn()

    def spawn(self):
        x = random.randint(0, GRID_WIDTH - 1) * GRID_SIZE
        y = random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        self.rect.topleft = (x, y)

class Player:
    def __init__(self, player_id, color):
        self.player_id = player_id
        self.snake = Snake(color, self.start_position())
        self.score = 0
        self.set_controls()

    def start_position(self):
        if self.player_id == 1:
            return (100, 100)
        elif self.player_id == 2:
            return (SCREEN_WIDTH - 100, SCREEN_HEIGHT - 100)

    def set_controls(self):
        if self.player_id == 1:
            self.controls = {
                pygame.K_UP: pygame.K_UP,
                pygame.K_DOWN: pygame.K_DOWN,
                pygame.K_LEFT: pygame.K_LEFT,
                pygame.K_RIGHT: pygame.K_RIGHT
            }
        elif self.player_id == 2:
            self.controls = {
                pygame.K_w: pygame.K_UP,
                pygame.K_s: pygame.K_DOWN,
                pygame.K_a: pygame.K_LEFT,
                pygame.K_d: pygame.K_RIGHT
            }

    def update_direction(self, key):
        if key in self.controls:
            new_direction = self.controls[key]
            # Prevent the snake from reversing
            opposite = {pygame.K_UP: pygame.K_DOWN, pygame.K_DOWN: pygame.K_UP,
                        pygame.K_LEFT: pygame.K_RIGHT, pygame.K_RIGHT: pygame.K_LEFT}
            if opposite[new_direction] != self.snake.direction:
                self.snake.direction = new_direction

# Main Game Class
class Game:
    def __init__(self, settings):
        self.settings = settings
        self.players = []
        self.food = Food()
        self.game_over = False

        # Initialize players
        colors = [self.settings['snake_color']]
        if self.settings['player_count'] == 2:
            colors.append((0, 0, 255))  # Second player color

        for i in range(self.settings['player_count']):
            player = Player(i+1, colors[i])
            self.players.append(player)

        self.all_sprites = pygame.sprite.Group()
        for player in self.players:
            for segment in player.snake.segments:
                self.all_sprites.add(segment)
        self.all_sprites.add(self.food)

    def run(self):
        clock = pygame.time.Clock()
        while not self.game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return 'quit'
                if event.type == pygame.KEYDOWN:
                    # Quit the game by pressing 'Q'
                    if event.key == pygame.K_q:
                        return 'quit'
                    for player in self.players:
                        player.update_direction(event.key)

            # Update game state
            for player in self.players:
                player.snake.move()

                # Update all sprites with new segments
                self.all_sprites.empty()
                for p in self.players:
                    for segment in p.snake.segments:
                        self.all_sprites.add(segment)
                self.all_sprites.add(self.food)

                if player.snake.check_collision():
                    self.game_over = True  # Game over

                # Check food collision
                if player.snake.head_rect.colliderect(self.food.rect):
                    player.snake.grow()
                    player.score += 10
                    self.food.spawn()

            # Check for collisions between snakes in two-player mode
            if len(self.players) == 2:
                # Player 1 collides with Player 2
                if self.check_snake_collision(self.players[0], self.players[1]):
                    self.game_over = True

                # Player 2 collides with Player 1
                if self.check_snake_collision(self.players[1], self.players[0]):
                    self.game_over = True

            # Render
            screen.fill(BLACK)
            for player in self.players:
                for segment in player.snake.segments:
                    screen.blit(segment.image, segment.rect)

            # Draw food
            screen.blit(self.food.image, self.food.rect)

            # Draw scores
            for idx, player in enumerate(self.players):
                score_text = f"Player {player.player_id} Score: {player.score}"
                draw_text(score_text, font_small, WHITE, screen, 100 + idx * 300, 20)

            pygame.display.flip()
            clock.tick(10)

        return 'game_over'

    def check_snake_collision(self, player1, player2):
        # Check if player1's head collides with any segment of player2
        head_pos = player1.snake.positions[0]
        if head_pos in player2.snake.positions:
            return True
        return False

    def get_scores(self):
        return {f'Player {p.player_id}': p.score for p in self.players}

# Main Menu Class
class MainMenu:
    def __init__(self):
        self.options = {
            'snake_color': (0, 255, 0),
            'player_count': 1
        }
        self.selected_color = 0
        self.colors = [(0, 255, 0), (255, 255, 0), (255, 0, 255), (0, 255, 255)]
        self.color_names = ["Green", "Yellow", "Magenta", "Cyan"]
        self.player_count = 1
        self.step = 1  # Step 1: Choose color, Step 2: Choose player count

    def run(self):
        while True:
            screen.fill(BLACK)
            draw_text("Snake Game", font_large, WHITE, screen, SCREEN_WIDTH // 2, 80)

            if self.step == 1:
                # Color selection
                draw_text("Select Snake Color:", font_small, WHITE, screen, SCREEN_WIDTH // 2, 150)
                for idx, color_name in enumerate(self.color_names):
                    color = WHITE if idx == self.selected_color else (100, 100, 100)
                    draw_text(color_name, font_small, color, screen, SCREEN_WIDTH // 2, 180 + idx * 30)
                draw_text("Press ENTER to confirm color", font_small, WHITE, screen, SCREEN_WIDTH // 2, 330)

            elif self.step == 2:
                # Player count selection
                draw_text("Select Player Count:", font_small, WHITE, screen, SCREEN_WIDTH // 2, 150)
                player_counts = [1, 2]
                for idx, count in enumerate(player_counts):
                    color = WHITE if count == self.player_count else (100, 100, 100)
                    draw_text(f"{count} Player", font_small, color, screen, SCREEN_WIDTH // 2, 180 + idx * 30)
                draw_text("Press ENTER to confirm player count", font_small, WHITE, screen, SCREEN_WIDTH // 2, 270)

            elif self.step == 3:
                # Ready to start
                draw_text("Press SPACE to Start the Game", font_small, WHITE, screen, SCREEN_WIDTH // 2, 200)

            pygame.display.flip()

            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if self.step == 1:
                        if event.key == pygame.K_UP:
                            if self.selected_color > 0:
                                self.selected_color -= 1
                        elif event.key == pygame.K_DOWN:
                            if self.selected_color < len(self.colors) - 1:
                                self.selected_color += 1
                        elif event.key == pygame.K_RETURN:
                            self.options['snake_color'] = self.colors[self.selected_color]
                            self.step = 2  # Move to next step
                    elif self.step == 2:
                        if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                            self.player_count = 1 if self.player_count == 2 else 2
                        elif event.key == pygame.K_RETURN:
                            self.options['player_count'] = self.player_count
                            self.step = 3  # Move to next step
                    elif self.step == 3:
                        if event.key == pygame.K_SPACE:
                            return self.options

# Game Over Screen Class
class GameOverScreen:
    def __init__(self, scores):
        self.scores = scores

    def run(self):
        while True:
            screen.fill(BLACK)
            draw_text("Game Over", font_large, RED, screen, SCREEN_WIDTH // 2, 80)

            # Display scores
            for idx, (player, score) in enumerate(self.scores.items()):
                score_text = f"{player} Score: {score}"
                draw_text(score_text, font_small, WHITE, screen, SCREEN_WIDTH // 2, 150 + idx * 30)

            # Instructions
            draw_text("Press R to Restart or Q to Quit", font_small, WHITE, screen, SCREEN_WIDTH // 2, 300)

            pygame.display.flip()

            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return 'quit'
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        return 'restart'
                    elif event.key == pygame.K_q:
                        return 'quit'

# Main Function
def main():
    game_state = STATE_MAIN_MENU
    main_menu = MainMenu()
    game = None
    game_over_screen = None
    running = True

    while running:
        if game_state == STATE_MAIN_MENU:
            selected_options = main_menu.run()
            if selected_options is not None:
                game = Game(selected_options)
                game_state = STATE_PLAYING

        elif game_state == STATE_PLAYING:
            result = game.run()
            if result == 'game_over':
                game_over_screen = GameOverScreen(game.get_scores())
                game_state = STATE_GAME_OVER
            elif result == 'quit':
                running = False

        elif game_state == STATE_GAME_OVER:
            action = game_over_screen.run()
            if action == 'restart':
                main_menu = MainMenu()  # Reset the menu to start fresh
                game_state = STATE_MAIN_MENU
            elif action == 'quit':
                running = False

        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
