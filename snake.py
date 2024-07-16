import pygame
import random

# Initialize Pygame
pygame.init()

# Get the screen size
SCREEN_WIDTH = pygame.display.Info().current_w
SCREEN_HEIGHT = pygame.display.Info().current_h

# Constants
GRID_PADDING = SCREEN_WIDTH // 10  # Padding around the grid
GRID_SIZE = min((SCREEN_WIDTH - 2 * GRID_PADDING) // 20, SCREEN_HEIGHT // 20) // 2  # Adjusted grid size based on padding and scaled down
GRID_WIDTH = (SCREEN_WIDTH - 2 * GRID_PADDING) // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
MAX_FOODS = 30  # Maximum number of food items to be present on the screen at a time

# Define 8 sets of bright color pairs for snake and food
color_sets = [
    {'snake': (255, 0, 0), 'food': (0, 255, 0)},    # Set 1: Red snake, Green food
    {'snake': (0, 255, 255), 'food': (255, 0, 255)},   # Set 2: Cyan snake, Magenta food
    {'snake': (255, 255, 0), 'food': (0, 0, 255)},   # Set 3: Yellow snake, Blue food
    {'snake': (255, 127, 0), 'food': (127, 0, 255)},   # Set 4: Orange snake, Purple food
    {'snake': (255, 0, 255), 'food': (0, 255, 255)},   # Set 5: Magenta snake, Cyan food
    {'snake': (0, 255, 0), 'food': (255, 255, 0)},   # Set 6: Green snake, Yellow food
    {'snake': (0, 0, 255), 'food': (255, 255, 255)},   # Set 7: Blue snake, White food
    {'snake': (127, 0, 255), 'food': (255, 127, 0)},   # Set 8: Purple snake, Orange food
    {'snake': (255, 0, 0), 'food': (255, 0, 0)}    # Set 9: Red snake, Red food
]

# Snake class
class Snake:
    def __init__(self):
        self.body = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = (1, 0)  # Start by moving to the right
        self.grow = False
        self.color_set_index = 0  # Start with the first color set
        self.color = color_sets[self.color_set_index]['snake']  # Initial snake color
        self.segment_size = GRID_SIZE  # Initial segment size
        self.snake_speed = int(10 * 1.25)  # Initial speed of the snake
        self.score = 0  # Initialize score
        self.multiplier = 0  # Initialize multiplier
        self.foods = []  # List to hold multiple food items
        self.paused = False  # Flag to track if the game is paused

    def update(self):
        if not self.paused:
            # Move the snake
            head_x, head_y = self.body[0]
            new_head = (head_x + self.direction[0], head_y + self.direction[1])

            # Check if the snake eats any food
            for food in self.foods[:]:
                if new_head == food.position:
                    self.grow = True
                    # Check if snake's color matches food's color
                    if self.color == food.color:
                        self.multiplier += 1
                    else:
                        self.multiplier = 0

                    # Calculate score based on new rules
                    self.score += 5 + self.multiplier * 10

                    self.foods.remove(food)

                    # Spawn new random number of foods (1-3)
                    num_new_foods = random.randint(1, 3)
                    for _ in range(num_new_foods):
                        if len(self.foods) < MAX_FOODS:
                            new_food = Food()
                            new_food.color = color_sets[random.randint(0, len(color_sets) - 1)]['food']  # Random color
                            self.foods.append(new_food)

                    # Change colors on food consumption
                    self.color_set_index = (self.color_set_index + 1) % len(color_sets)
                    self.color = color_sets[self.color_set_index]['snake']

            # Add new head
            self.body.insert(0, new_head)

            # If not growing, remove the tail
            if not self.grow:
                self.body.pop()
            else:
                self.grow = False

            # Increase snake speed with its length
            self.snake_speed = 5 + len(self.body) // 3

    def change_direction(self, direction):
        if direction == 'UP' and self.direction != (0, 1):
            self.direction = (0, -1)
        elif direction == 'DOWN' and self.direction != (0, -1):  # Adjusted condition
            self.direction = (0, 1)
        elif direction == 'LEFT' and self.direction != (1, 0):
            self.direction = (-1, 0)
        elif direction == 'RIGHT' and self.direction != (-1, 0):
            self.direction = (1, 0)
        elif direction == 'PAUSE':
            self.paused = not self.paused  # Toggle pause state

    def check_collision(self):
        # Check wall collision
        head_x, head_y = self.body[0]
        if head_x < 0 or head_x >= GRID_WIDTH or head_y < 0 or head_y >= GRID_HEIGHT:
            return True

        # Check self collision
        if len(self.body) != len(set(self.body)):
            return True

        return False

    def draw(self, screen):
        for segment in self.body:
            pygame.draw.rect(screen, self.color, (segment[0] * GRID_SIZE + GRID_PADDING, segment[1] * GRID_SIZE, self.segment_size, self.segment_size))
        
        for food in self.foods:
            food.draw(screen)

        # Display score outside play area
        display_text(screen, f"Score: {self.score}", (255, 255, 255), SCREEN_WIDTH - GRID_PADDING - 180, 20, align="right")

        # Display multiplier below the score
        display_text(screen, f"Multiplier: {self.multiplier}", (255, 255, 255), SCREEN_WIDTH - GRID_PADDING - 180, 60, align="right")

        # Display pause message if paused
        if self.paused:
            display_text(screen, "Paused", (255, 255, 255), SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)


# Food class
class Food:
    def __init__(self):
        self.base_radius = GRID_SIZE / 2
        self.position = self.randomize_position()
        self.color = color_sets[0]['food']  # Initial food color

    def randomize_position(self):
        while True:
            position = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
            if position[0] != 0 and position[0] != GRID_WIDTH - 1 and position[1] != 0 and position[1] != GRID_HEIGHT - 1:
                return position

    def draw(self, screen):
        # Draw the food as a circle
        center_x = (self.position[0] + 0.5) * GRID_SIZE + GRID_PADDING
        center_y = (self.position[1] + 0.5) * GRID_SIZE
        pygame.draw.circle(screen, self.color, (int(center_x), int(center_y)), int(self.base_radius))


# Game states
class GameState:
    def __init__(self):
        self.game_over = False
        self.restart = False
        self.start_screen = True
        self.end_screen = False

    def reset(self):
        self.game_over = False
        self.restart = False
        self.start_screen = True
        self.end_screen = False


# Function to display text with modern font
def display_text(screen, text, color, x, y, align="left"):
    font = pygame.font.Font(pygame.font.get_default_font(), 36)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()

    if align == "right":
        text_rect.right = x
    elif align == "center":
        text_rect.centerx = x
    else:
        text_rect.left = x

    text_rect.y = y
    screen.blit(text_surface, text_rect)


# Main function
def main():
    # Initialize game state
    game_state = GameState()

    # Set up the screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Snake Game')

    # Initialize clock
    clock = pygame.time.Clock()

    # Initialize snake and food
    snake = Snake()
    initial_food = Food()
    initial_food.color = color_sets[0]['food']
    snake.foods.append(initial_food)

    # Main game loop
    while True:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.KEYDOWN:
                if game_state.start_screen:
                    game_state.start_screen = False  # Start the game on any key press
                elif event.key == pygame.K_UP:
                    snake.change_direction('UP')
                elif event.key == pygame.K_DOWN:
                    snake.change_direction('DOWN')
                elif event.key == pygame.K_LEFT:
                    snake.change_direction('LEFT')
                elif event.key == pygame.K_RIGHT:
                    snake.change_direction('RIGHT')
                elif event.key == pygame.K_p:
                    snake.change_direction('PAUSE')  # Toggle pause state
                elif game_state.game_over:
                    if event.key == pygame.K_r:  # Restart game
                        game_state.reset()
                        snake = Snake()  # Reset snake
                        initial_food = Food()
                        initial_food.color = color_sets[0]['food']
                        snake.foods.append(initial_food)  # Reset initial food
                    elif event.key == pygame.K_q:  # Quit game
                        return

        # Start screen
        if game_state.start_screen:
            screen.fill((0, 0, 0))  # Black background
            display_text(screen, "Press R to start", (255, 255, 255), SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, align="center")
            display_text(screen, "Use arrow keys to move the snake. Press P to pause.", (255, 255, 255), SCREEN_WIDTH // 2, SCREEN_HEIGHT - 40, align="center")
            pygame.display.flip()
            continue

        # Game over screen
        if game_state.game_over:
            screen.fill((0, 0, 0))  # Black background
            pygame.draw.rect(screen, (255, 105, 180), (GRID_PADDING, 0, SCREEN_WIDTH - 2 * GRID_PADDING, SCREEN_HEIGHT), 3)
            display_text(screen, "Game Over", (255, 255, 255), SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50, align="center")
            display_text(screen, f"Score: {snake.score}", (255, 255, 255), SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, align="center")
            display_text(screen, f"Multiplier: {snake.multiplier}", (255, 255, 255), SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50, align="center")
            display_text(screen, "Press R to restart or Q to quit", (255, 255, 255), SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100, align="center")
            pygame.display.flip()

            # Reset the clock to limit frame rate for end screen
            clock.tick(10)
            continue

        # Update game state
        if not game_state.start_screen and not game_state.game_over:
            snake.update()
            if snake.check_collision():
                game_state.game_over = True

        # Drawing on screen
        screen.fill((0, 0, 0))  # Black background
        pygame.draw.rect(screen, (255, 105, 180), (GRID_PADDING, 0, SCREEN_WIDTH - 2 * GRID_PADDING, SCREEN_HEIGHT), 3)

        # Draw snake and food
        snake.draw(screen)

        # Update display
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(snake.snake_speed)  # Adjust speed by changing this value


if __name__ == '__main__':
    main()
