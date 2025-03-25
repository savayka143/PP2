import pygame, sys, random

# Initialize Pygame
pygame.init()
clock = pygame.time.Clock()

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED   = (255, 0, 0)
BLUE  = (0, 0, 255)

# Screen dimensions and snake block size
WIDTH = 600
HEIGHT = 400
BLOCK_SIZE = 20

# Create display window and set title
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game with Weighted Food and Timer")

# Set up font for score and level display
font = pygame.font.SysFont(None, 35)

def draw_text(text, color, x, y):
    """Helper function to draw text on the screen."""
    img = font.render(text, True, color)
    screen.blit(img, (x, y))

def get_random_food_position(snake):
    """
    Generate a random position for the food.
    Ensures the food does not appear on the snake's body.
    """
    while True:
        x = random.randint(0, (WIDTH - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        y = random.randint(0, (HEIGHT - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        if (x, y) not in snake:
            return (x, y)

# Food class for creating food with weight and a disappearance timer
class Food:
    def __init__(self, snake):
        # Generate food position ensuring it does not collide with the snake
        self.position = get_random_food_position(snake)
        # Assign a random weight: 1, 2, or 3. The weight is added to the score when eaten.
        self.weight = random.choice([1, 2, 3])
        # Set the food color based on its weight for visual differentiation
        if self.weight == 1:
            self.color = RED
        elif self.weight == 2:
            self.color = BLUE
        else:
            self.color = GREEN
        # Record the spawn time of the food (in milliseconds)
        self.spawn_time = pygame.time.get_ticks()

    def draw(self, surface):
        """Draw the food on the given surface."""
        pygame.draw.rect(surface, self.color, (self.position[0], self.position[1], BLOCK_SIZE, BLOCK_SIZE))

# Initialize snake parameters
snake = [(WIDTH // 2, HEIGHT // 2)]  # Snake starts at the center of the screen
direction = (0, 0)                   # No movement until a key is pressed
score = 0                            # Initial score
level = 1                            # Initial level
foods_eaten = 0                      # Counter for foods eaten (for level progression)
speed = 5                          # Initial game speed (frames per second)

# Food lifetime (in milliseconds). For example, 5000 = 5 seconds.
FOOD_LIFETIME = 5000

# Generate the first food object
food = Food(snake)

running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # Handle arrow key inputs to change direction
        elif event.type == pygame.KEYDOWN:
            # Prevent the snake from reversing into itself
            if event.key == pygame.K_UP and direction != (0, BLOCK_SIZE):
                direction = (0, -BLOCK_SIZE)
            elif event.key == pygame.K_DOWN and direction != (0, -BLOCK_SIZE):
                direction = (0, BLOCK_SIZE)
            elif event.key == pygame.K_LEFT and direction != (BLOCK_SIZE, 0):
                direction = (-BLOCK_SIZE, 0)
            elif event.key == pygame.K_RIGHT and direction != (-BLOCK_SIZE, 0):
                direction = (BLOCK_SIZE, 0)

    # Only move the snake if a direction is set
    if direction != (0, 0):
        # Calculate the new head position based on the current direction
        head_x, head_y = snake[0]
        dx, dy = direction
        new_head = (head_x + dx, head_y + dy)

        # Check for collision with walls
        if new_head[0] < 0 or new_head[0] >= WIDTH or new_head[1] < 0 or new_head[1] >= HEIGHT:
            running = False  # End game if collision occurs

        # Check for collision with itself
        if new_head in snake:
            running = False  # End game if the snake collides with itself

        # Insert the new head at the beginning of the snake list (move forward)
        snake.insert(0, new_head)

        # Check if the snake eats the food (head collides with food)
        if new_head == food.position:
            score += food.weight      # Add the weight of the food to the score
            foods_eaten += 1          # Increase the count of foods eaten
            food = Food(snake)        # Generate a new food object
            # Increase level and speed every 3 foods eaten (example threshold)
            if foods_eaten % 3 == 0:
                level += 1
                speed += 2
        else:
            # If food is not eaten, remove the tail block (snake moves forward)
            snake.pop()

    # Check if the food's lifetime has expired
    current_time = pygame.time.get_ticks()
    if current_time - food.spawn_time > FOOD_LIFETIME:
        # If the food "expires", generate a new one
        food = Food(snake)

    # Fill the screen with a white background
    screen.fill(WHITE)

    # Draw each block of the snake
    for block in snake:
        pygame.draw.rect(screen, GREEN, (block[0], block[1], BLOCK_SIZE, BLOCK_SIZE))

    # Draw the food on the screen
    food.draw(screen)

    # Display the score and level in the top corners of the screen
    draw_text("Score: " + str(score), BLACK, 10, 10)
    draw_text("Level: " + str(level), BLACK, WIDTH - 120, 10)

    pygame.display.update()
    clock.tick(speed)  # Control game speed based on the current level

pygame.quit()
sys.exit()
