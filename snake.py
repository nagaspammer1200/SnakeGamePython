import pygame
import random
import time
import math

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
MAX_FOODS = 3  # Maximum number of foods to eat before ending the game

# Define 8 sets of bright color pairs for snake and food
color_sets = [
    {'snake': (255, 0, 0), 'food': (0, 255, 0)},    # Set 1: Red snake, Green food
    {'snake': (0, 255, 255), 'food': (255, 0, 255)},   # Set 2: Cyan snake, Magenta food
    {'snake': (255, 255, 0), 'food': (0, 0, 255)},   # Set 3: Yellow snake, Blue food
    {'snake': (255, 127, 0), 'food': (127, 0, 255)},   # Set 4: Orange snake, Purple food
    {'snake': (255, 0, 255), 'food': (0, 255, 255)},   # Set 5: Magenta snake, Cyan food
    {'snake': (0, 255, 0), 'food': (255, 255, 0)},   # Set 6: Green snake, Yellow food
    {'snake': (0, 0, 255), 'food': (255, 255, 255)},   # Set 7: Blue snake, White food
    {'snake': (127, 0, 255), 'food': (255, 127, 0)}    # Set 8: Purple snake, Orange food
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
        self.snake_speed = int(10 * 1.65)  # Initial speed of the snake
        self.speed_increase_rate = 1.3
        self.score = 0  # Initialize score

    def update(self, food):
        # Move the snake
        head_x, head_y = self.body[0]
        new_head = (head_x + self.direction[0], head_y + self.direction[1])

        # Check if the snake eats food
        if new_head == food.position:
            self.grow = True
            food.randomize_position()

            # Increment score by 10 on food consumption
            self.score += 10

            # Change colors on food consumption
            self.color_set_index = (self.color_set_index + 1) % len(color_sets)
            self.color = color_sets[self.color_set_index]['snake']
            food.color = color_sets[self.color_set_index]['food']

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
        elif direction == 'DOWN' and self.direction != (0, -1):
            self.direction = (0, 1)
        elif direction == 'LEFT' and self.direction != (1, 0):
            self.direction = (-1, 0)
        elif direction == 'RIGHT' and self.direction != (-1, 0):
            self.direction = (1, 0)

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


# Food class
class Food:
    def __init__(self):
        self.base_radius = GRID_SIZE / 2
        self.position = self.randomize_position()
        self.color = color_sets[0]['food']  # Initial food color
        self.pulse_color = (255, 255, 255)  # Color for pulse effect
        self.pulse_duration = 1.5  # Duration of pulse effect in seconds
        self.pulse_start_time = time.time()

    def randomize_position(self):
        while True:
            position = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
            if position[0] != 0 and position[0] != GRID_WIDTH - 1 and position[1] != 0 and position[1] != GRID_HEIGHT - 1:
                return position

    def update(self):
        # Pulse effect for food
        if time.time() - self.pulse_start_time > self.pulse_duration:
            self.pulse_color = (255, 255, 255)  # Reset pulse color
            self.pulse_start_time = time.time()

    def draw(self, screen):
        self.update()  # Update pulse effect
        # Calculate pulse scale based on time
        pulse_scale = 1.0 + 1.0 * math.sin(2 * math.pi * (time.time() - self.pulse_start_time) / self.pulse_duration)
        radius = self.base_radius * pulse_scale
        center_x = (self.position[0] + 0.5) * GRID_SIZE + GRID_PADDING
        center_y = (self.position[1] + 0.5) * GRID_SIZE
        pygame.draw.circle(screen, self.pulse_color, (int(center_x), int(center_y)), int(radius))


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


# Function to display text
def display_text(screen, text, color, x, y):
    font = pygame.font.Font(None, 36)
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))


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
    food = Food()

    # Game loop
    while True:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.KEYDOWN:
                if game_state.start_screen:
                    game_state.start_screen = False  # Exit start screen on any key press
                elif event.key == pygame.K_UP:
                    snake.change_direction('UP')
                elif event.key == pygame.K_DOWN:
                    snake.change_direction('DOWN')
                elif event.key == pygame.K_LEFT:
                    snake.change_direction('LEFT')
                elif event.key == pygame.K_RIGHT:
                    snake.change_direction('RIGHT')

        # Start screen
        if game_state.start_screen:
            screen.fill((0, 0, 0))  # Black background
            display_text(screen, "Press any key to start", (255, 255, 255), SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 50)
            pygame.display.flip()
            continue  # Skip the rest of the game loop until any key is pressed

        # Update snake
        if not game_state.game_over:
            snake.update(food)

            # Check for collision
            if snake.check_collision():
                game_state.game_over = True

            # Check if food is eaten
            if snake.body[0] == food.position:
                snake.grow = True
                food.position = food.randomize_position()

                # Change colors on food consumption
                snake.color_set_index = (snake.color_set_index + 1) % len(color_sets)
                snake.color = color_sets[snake.color_set_index]['snake']
                food.color = color_sets[snake.color_set_index]['food']

        # Clear screen
        screen.fill((0, 0, 0))  # Black background

        # Draw playable area border
        pygame.draw.rect(screen, (255, 105, 180), (GRID_PADDING, 0, SCREEN_WIDTH - 2 * GRID_PADDING, SCREEN_HEIGHT), 3)

        # Draw snake and food
        snake.draw(screen)
        food.draw(screen)

        # Display score
        display_text(screen, f"Score: {snake.score}", (255, 255, 255), GRID_PADDING + 20, 20)

        # Update display
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(snake.snake_speed)  # Adjust speed by changing this value

        # End screen
        while game_state.game_over:
            screen.fill((0, 0, 0))  # Black background
            pygame.draw.rect(screen, (255, 105, 180), (GRID_PADDING, 0, SCREEN_WIDTH - 2 * GRID_PADDING, SCREEN_HEIGHT), 3)
            display_text(screen, "Game Over", (255, 255, 255), SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50)
            display_text(screen, f"Score: {snake.score}", (255, 255, 255), SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 2)
            display_text(screen, "Press R to restart or Q to quit", (255, 255, 255), SCREEN_WIDTH // 2 - 180, SCREEN_HEIGHT // 2 + 50)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        game_state.reset()
                        snake = Snake()  # Reset snake
                        food = Food()    # Reset food
                    elif event.key == pygame.K_q:
                        return


if __name__ == '__main__':
    main()
