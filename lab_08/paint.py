import pygame, sys, math
pygame.init()

# Define colors
WHITE   = (255, 255, 255)
BLACK   = (0, 0, 0)
RED     = (255, 0, 0)
GREEN   = (0, 255, 0)
BLUE    = (0, 0, 255)
YELLOW  = (255, 255, 0)
PURPLE  = (128, 0, 128)
ORANGE  = (255, 165, 0)
GRAY    = (200, 200, 200)

# Window dimensions and toolbar height
WIDTH = 800
HEIGHT = 600
TOOLBAR_HEIGHT = 60

# Set up the main screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint Application")
clock = pygame.time.Clock()

# Create a separate canvas surface (drawing area) below the toolbar
canvas = pygame.Surface((WIDTH, HEIGHT - TOOLBAR_HEIGHT))
canvas.fill(WHITE)

# Define drawing modes
MODE_FREE   = 'free'
MODE_RECT   = 'rectangle'
MODE_CIRCLE = 'circle'
MODE_ERASER = 'eraser'
draw_mode = MODE_FREE    # default mode is free drawing

current_color = BLACK    # default drawing color
brush_size = 5           # brush size for drawing

# Set up font for toolbar buttons
button_font = pygame.font.SysFont(None, 24)

# Define toolbar buttons dimensions and padding
button_width = 100
button_height = 40
padding = 10
start_x = padding
start_y = (TOOLBAR_HEIGHT - button_height) // 2

# Create tool buttons: Free Draw, Rectangle, Circle, Eraser
tool_buttons = []
tools = [
    {'label': 'Free',   'mode': MODE_FREE},
    {'label': 'Rect',   'mode': MODE_RECT},
    {'label': 'Circle', 'mode': MODE_CIRCLE},
    {'label': 'Eraser', 'mode': MODE_ERASER}
]
for tool in tools:
    btn_rect = pygame.Rect(start_x, start_y, button_width, button_height)
    tool_buttons.append({'label': tool['label'], 'mode': tool['mode'], 'rect': btn_rect})
    start_x += button_width + padding

# Create color selection buttons for a few colors
colors = [BLACK, RED, GREEN, BLUE, YELLOW, PURPLE, ORANGE]
color_buttons = []
for col in colors:
    btn_rect = pygame.Rect(start_x, start_y, button_width, button_height)
    color_buttons.append({'color': col, 'rect': btn_rect})
    start_x += button_width + padding

# Variables to keep track of drawing state
drawing = False    # flag for when the user is drawing
start_pos = None   # starting position for shapes

# Main loop
running = True
while running:
    clock.tick(60)  # Limit frame rate to 60 FPS
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Handle mouse button down events
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            # Check if the click is in the toolbar area
            if pos[1] < TOOLBAR_HEIGHT:
                # Check if a tool button was clicked
                for btn in tool_buttons:
                    if btn['rect'].collidepoint(pos):
                        draw_mode = btn['mode']
                # Check if a color button was clicked
                for btn in color_buttons:
                    if btn['rect'].collidepoint(pos):
                        current_color = btn['color']
                        # If user picks a color while in eraser mode, switch to free draw
                        if draw_mode == MODE_ERASER:
                            draw_mode = MODE_FREE
            else:
                # Click occurred in the drawing canvas; adjust y coordinate relative to canvas
                canvas_pos = (pos[0], pos[1] - TOOLBAR_HEIGHT)
                drawing = True
                start_pos = canvas_pos
                # For free drawing or eraser, draw an initial dot to capture the click
                if draw_mode in [MODE_FREE, MODE_ERASER]:
                    color_to_use = WHITE if draw_mode == MODE_ERASER else current_color
                    pygame.draw.circle(canvas, color_to_use, canvas_pos, brush_size)
        
        # Handle mouse motion events (only draw when the mouse is held down)
        if event.type == pygame.MOUSEMOTION:
            if drawing:
                pos = pygame.mouse.get_pos()
                canvas_pos = (pos[0], pos[1] - TOOLBAR_HEIGHT)
                if draw_mode in [MODE_FREE, MODE_ERASER]:
                    color_to_use = WHITE if draw_mode == MODE_ERASER else current_color
                    # Draw a line from the previous position to the current position
                    pygame.draw.line(canvas, color_to_use, start_pos, canvas_pos, brush_size * 2)
                    start_pos = canvas_pos
        
        # Handle mouse button up events to complete shape drawing
        if event.type == pygame.MOUSEBUTTONUP:
            if drawing:
                pos = pygame.mouse.get_pos()
                end_pos = (pos[0], pos[1] - TOOLBAR_HEIGHT)
                if draw_mode == MODE_RECT:
                    # Calculate rectangle dimensions from the start and end positions
                    rect_x = min(start_pos[0], end_pos[0])
                    rect_y = min(start_pos[1], end_pos[1])
                    rect_width = abs(end_pos[0] - start_pos[0])
                    rect_height = abs(end_pos[1] - start_pos[1])
                    # Draw the rectangle outline (change the last parameter to 0 for filled)
                    pygame.draw.rect(canvas, current_color, (rect_x, rect_y, rect_width, rect_height), brush_size)
                elif draw_mode == MODE_CIRCLE:
                    # Calculate the radius as the Euclidean distance between start and end points
                    radius = int(math.hypot(end_pos[0] - start_pos[0], end_pos[1] - start_pos[1]))
                    # Draw the circle outline (change the last parameter to 0 for filled)
                    pygame.draw.circle(canvas, current_color, start_pos, radius, brush_size)
                drawing = False
                start_pos = None

    # --- Drawing the UI ---

    # Draw the toolbar background
    pygame.draw.rect(screen, GRAY, (0, 0, WIDTH, TOOLBAR_HEIGHT))
    
    # Draw tool selection buttons
    for btn in tool_buttons:
        pygame.draw.rect(screen, WHITE, btn['rect'])
        text = button_font.render(btn['label'], True, BLACK)
        text_rect = text.get_rect(center=btn['rect'].center)
        screen.blit(text, text_rect)
    
    # Draw color selection buttons
    for btn in color_buttons:
        pygame.draw.rect(screen, btn['color'], btn['rect'])
        # Draw a border around each color button
        pygame.draw.rect(screen, BLACK, btn['rect'], 2)
    
    # Blit the drawing canvas onto the main screen
    screen.blit(canvas, (0, TOOLBAR_HEIGHT))
    
    pygame.display.flip()

pygame.quit()
sys.exit()
