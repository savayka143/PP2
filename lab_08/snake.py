import pygame, sys, random

# Initialize Pygame
pygame.init()
clock = pygame.time.Clock()

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED   = (255, 0, 0)

# Screen dimensions and snake block size
WIDTH = 600
HEIGHT = 400
BLOCK_SIZE = 20

# Create display window and set title
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game with Levels")

# Set up font for score and level display
font = pygame.font.SysFont(None, 35)

def draw_text(text, color, x, y):
    """Helper function to draw text on the screen."""
    img = font.render(text, True, color)
    screen.blit(img, (x, y))

def get_food_position(snake):
    """
    Generate a random position for food.
    Ensures the food does not appear on the snake's body.
    """
    while True:
        x = random.randint(0, (WIDTH - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        y = random.randint(0, (HEIGHT - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        if (x, y) not in snake:  # Ensure food is not spawned on the snake
            return (x, y)

# Initialize snake parameters
snake = [(WIDTH // 2, HEIGHT // 2)]  # Snake starts at the center
direction = (0, 0)                   # No movement until a key is pressed
score = 0                            # Initial score
level = 1                            # Initial level
foods_eaten = 0                      # Counter for foods eaten (used for level progression)
speed = 10                           # Initial game speed (frames per second)

# Place the first food
food = get_food_position(snake)

running = True
while running:
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
    
    # Only move the snake if a direction has been set
    if direction != (0, 0):
        # Calculate new head position based on current direction
        head_x, head_y = snake[0]
        dx, dy = direction
        new_head = (head_x + dx, head_y + dy)
        
        # Check for wall collision (snake hitting borders)
        if new_head[0] < 0 or new_head[0] >= WIDTH or new_head[1] < 0 or new_head[1] >= HEIGHT:
            running = False  # End game if collision occurs
        
        # Check for collision with itself
        if new_head in snake:
            running = False  # End game if snake runs into itself
        
        # Insert the new head to the beginning of the snake list
        snake.insert(0, new_head)
        
        # Check if food is eaten (snake's head collides with food)
        if new_head == food:
            score += 1          # Increase score
            foods_eaten += 1    # Increase food counter for level progression
            food = get_food_position(snake)  # Generate a new food position
            # Increase level and speed every 3 foods eaten (example threshold)
            if foods_eaten % 3 == 0:
                level += 1
                speed += 2      # Increase game speed as level increases
        else:
            # Remove the tail block if food was not eaten (snake moves forward)
            snake.pop()
    
    # Fill screen with white background
    screen.fill(WHITE)
    
    # Draw the snake blocks
    for block in snake:
        pygame.draw.rect(screen, GREEN, (block[0], block[1], BLOCK_SIZE, BLOCK_SIZE))
    
    # Draw the food block
    pygame.draw.rect(screen, RED, (food[0], food[1], BLOCK_SIZE, BLOCK_SIZE))
    
    # Display score and level counters at the top of the screen
    draw_text("Score: " + str(score), BLACK, 10, 10)
    draw_text("Level: " + str(level), BLACK, WIDTH - 120, 10)
    
    pygame.display.update()
    clock.tick(speed)  # Control the game speed based on the current level

pygame.quit()
sys.exit()
