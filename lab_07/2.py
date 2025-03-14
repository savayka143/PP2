import pygame
import sys
from pygame.locals import *

pygame.init()
pygame.mixer.init()

songs = ["song1.mp3", "song2.mp3", "song3.mp3"]
current_song_index = 0
status_message = "Press Z to play, X to stop, C for next, V for previous."

def play_song(index):
    """Load and play the song at the given index and update the status message."""
    global status_message
    try:
        pygame.mixer.music.load(songs[index])
        pygame.mixer.music.play()
        status_message = f"Playing: {songs[index]}"
        print(status_message)
    except Exception as e:
        status_message = "Error playing song: " + str(e)
        print(status_message)

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Music Player")
font = pygame.font.Font(None, 36)
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == pygame.K_z:
                play_song(current_song_index)
            elif event.key == pygame.K_x:
                pygame.mixer.music.stop()
                status_message = "Playback stopped."
                print(status_message)
            elif event.key == pygame.K_c:
                current_song_index = (current_song_index + 1) % len(songs)
                play_song(current_song_index)
            elif event.key == pygame.K_v:
                current_song_index = (current_song_index - 1) % len(songs)
                play_song(current_song_index)
    
    screen.fill((30, 30, 30))
    
    text_surface = font.render(status_message, True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=(400, 300))
    screen.blit(text_surface, text_rect)
    
    pygame.display.flip()
    clock.tick(30)