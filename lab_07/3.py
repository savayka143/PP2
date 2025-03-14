import pygame
import sys

pygame.init()

width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Moving Red Ball")

ball_color = (255, 0, 0)       
ball_radius = 25               
ball_x = width // 2            
ball_y = height // 2           
move_step = 20                 

clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if ball_y - move_step >= ball_radius:
                    ball_y -= move_step
            elif event.key == pygame.K_DOWN:
                if ball_y + move_step <= height - ball_radius:
                    ball_y += move_step
            elif event.key == pygame.K_LEFT:
                if ball_x - move_step >= ball_radius:
                    ball_x -= move_step
            elif event.key == pygame.K_RIGHT:
                if ball_x + move_step <= width - ball_radius:
                    ball_x += move_step
    
    screen.fill((255, 255, 255))
    
    pygame.draw.circle(screen, ball_color, (ball_x, ball_y), ball_radius)
    
    pygame.display.flip()
    
    clock.tick(30)

pygame.quit()
sys.exit()