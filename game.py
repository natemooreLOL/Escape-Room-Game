import pygame
pygame.init()

from game_setup import play_game

pygame.mixer.init()
pygame.mixer.music.load('labyrinth_escape.ogg')
pygame.mixer.music.set_volume(0.3) # Ears will no longer bleed when the music starts
pygame.mixer.music.play(-1)  # Loops the music indefinitely



play_game()