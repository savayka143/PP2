import pygame as pg
import sys
from datetime import datetime
import math

pg.init()

W = 1000
H = 800
H_WIDTH, H_HEIGHT = W // 2, H // 2
RADIUS = H_HEIGHT - 50

sc = pg.display.set_mode((W, H))
pg.display.set_caption("Clock")
clock_obj = pg.time.Clock() 

# Loading images
clock_img = pg.image.load('clock.png')
min_hand = pg.image.load('min_hand.png')
sec_hand = pg.image.load('sec_hand.png')

# Clock face's center
clock_rect = clock_img.get_rect(center=(H_WIDTH, H_HEIGHT))

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()

    # Сlearing the screen and drawing the dial
    sc.fill(pg.Color('white'))
    sc.blit(clock_img, clock_rect)

    # Getting current time
    t = datetime.now()

    # Calculate the rotation angle for the minute and second hands
    hour = ((t.hour % 12) * 5 + t.minute // 12)
    minute = t.minute 
    seconds = t.second

    min_angle = -(minute * 6 + seconds * 0.1) - 42
    sec_angle = -seconds * 6

    # Rotate the arrow images
    rotated_min_hand = pg.transform.rotate(min_hand, min_angle)
    rotated_sec_hand = pg.transform.rotate(sec_hand, sec_angle)

    # Calculate new rectangles to keep the arrows in the center
    min_rect = rotated_min_hand.get_rect(center=(H_WIDTH, H_HEIGHT))
    sec_rect = rotated_sec_hand.get_rect(center=(H_WIDTH, H_HEIGHT))

    # Drawing the arrows
    sc.blit(rotated_min_hand, min_rect)
    sc.blit(rotated_sec_hand, sec_rect)

    pg.display.update()
    clock_obj.tick(60)