import sys

import pygame
from pygame.locals import *
from Code.scripts.player import Player

# Game Plan
# Rpg Style Maze
# Player Moves all 4 directions
# Walls Will be HUGE pumpkins
# Behind you is the grimp reaper
# The maze has candy littered around it
# The goal is to get all candy
# Maze will stay the same but the candy location will be random for every instance of the game
#
#
# TODO
# Add Player Sprite
# Draw and Add Walls
# Add Tiled Map support
# Add Candy scipt that can be added Anywhere


pygame.init()

fps = 60
fpsClock = pygame.time.Clock()







width, height = 1280, 720
dispwidth, dispheight = 320 / 2, 180 / 2
screen = pygame.display.set_mode((width, height))
disp = pygame.Surface((dispwidth, dispheight))

player = Player()

# Game loop.
while True:
    disp.fill((255, 255, 255))

    for event in pygame.event.get():
        player.Event(event)
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # Update.
    player.Update()
    # Draw.
    player.Draw(disp)

    screen.blit(pygame.transform.scale(disp, (width, height)), (0, 0))
    pygame.display.flip()
    fpsClock.tick(fps)