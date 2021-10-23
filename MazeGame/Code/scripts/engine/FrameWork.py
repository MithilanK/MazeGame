# Import -----------------------------------------------------------  #

import math
import os

import pygame
import json
import sys
import math as m
import time
from pygame.locals import *


# FrameWork ------------------------------------------------------------  #

# TODO
# 1. Entity System -- Done
# 2. Animation System -- Done
# 3. Parallax Scrolling -- Done
# 4. Sound Effect System// Background Music Configurable -- Done
# 5. Game Class// Delta Game, Ticked Game, Fixed Game -- Done
# 6. Time system where you can slow down and speed up time -- Done
# 7. Leaf Flowing Effect -- WIP
# 8. Tiled map loader - Done
# 9. Slope Tiles -- WIP

# Core_Funcs -----------------------------------------------------------  #


# A shortcut to loading img's
def load_img(path):
    img = pygame.image.load(path).convert()
    return img


# A shortcut to loading sounds's
def load_sound(path):
    sound = pygame.mixer.Sound(path)
    return sound


# Initialize sound
def init_sound():
    pygame.mixer.pre_init(44100, -16, 2, 512)


# Load Map based on map
def load_map(path):
    f = open(path, 'r')
    data = f.read()
    f.close()
    data = data.split('\n')
    game_map = []
    for row in data:
        game_map.append(list(row))
    return game_map


# Angle Calculator
def AngleCalculator(Ad, Op):
    hype = math.hypot(Ad, Op)
    sinnum = Op / hype
    return -m.degrees(m.asin(sinnum))

# Distance Between Two Points
def distancebetweentwopoints(coord1, coord2):
    lenx = coord2[0] - coord1[0]
    leny = coord2[1] - coord1[0]
    distance = m.hypot(lenx, leny)
    return distance

def differencebetweentwopoints(coord1, coord2):
    lenx = coord2[0] - coord1[0]
    leny = coord2[1] - coord1[0]
    return [lenx, leny]


#MoveTowards
def MoveTowards(E, pos):
    towards = pygame.math.Vector2(E.hitbox.x - pos[0], E.hitbox.y - pos[1])
    towards = towards.normalize()
    towards *= 5
    return [towards.x , towards.y]


# Core_Classes ------------------------------------------------------------  #

# Time configurable (used for slow mo effects)
class Time:
    def __init__(self):
        self.dt = 0

    def scale(self, dt, percent):
        dtt = (dt / 100) * percent
        return dtt


# A Sound Effect For a Game
class Sound:
    def __init__(self, fx):
        self.Fx = fx

    def play(self):
        pygame.mixer.Sound.play(self.Fx)


# A Music that can be played in a game
class Music:
    def __init__(self, path):
        self.SongPath = path

    def play(self):
        pygame.mixer.music.load(self.SongPath)
        pygame.mixer.music.play()


# A game that runs at the max speed of the computed and updates at a fixed speed throught delta time
class DeltaGame:

    def create(self):
        pass

    def update(self, dt):
        pass

    def run(self):
        self.running = True
        self.create()
        Clock = pygame.time.Clock()
        dt = 1
        while self.running:
            self.update(dt)
            Clock.tick(60)

    def __init__(self, logicspeed):
        self.logicspeed = logicspeed
        self.running = False


# A game tha runs at a fixed speed of fps
class FixedGame:
    def create(self):
        pass

    def update(self):
        pass

    def run(self):
        Clock = pygame.time.Clock
        self.running = True
        self.create()
        while self.running:
            self.update()
            Clock.tick(self.fps)

    def __init__(self, Fps):
        self.fps = Fps
        self.running = False


# A game that draws to the screen at the max speed of the computer but updates the game state at a fixed speed
class TickedGame:
    def create(self):
        pass

    def update(self):
        pass

    def render(self):
        pass

    def run(self):
        last_time = time.time()
        self.create()
        while self.running:
            self.render()
            if last_time + self.tbt >= time.time():
                self.update()

    def __init__(self, Tps):
        self.tps = Tps
        self.running = True
        self.tbt = 1 / Tps
        self.run()


# Parralax Layer follows player at set speed
class ParallaxLayer:
    def __init__(self, img, z):
        self.img = img
        self.x, self.y = 0, 0
        self.speed = z / 100

        self.oldcamera = [0, 0]

    def update(self, camera, entity):
        self.x += (camera.x - entity.hitbox.x) * self.speed
        self.y += (camera.y - entity.hitbox.y) * self.speed

    def draw(self, main):
        main.blit(self.img, (self.x, self.y))


# Frame Independent Animation
class Animation:
    def __init__(self, frames, speed):
        self.frames = frames
        self.frame = 0
        self.speed = speed
        self.playing = False
        self.tbf = self.speed / len(self.frames)
        self.lastframetime = time.time()
        self.img = frames[0]

    def play(self):
        if self.playing:
            pass
        else:
            self.playing = True
            self.lastframetime = time.time()

    def pause(self):
        self.playing = False

    def unpause(self):
        self.playing = True

    def restart(self):
        self.frame = 0
        self.playing = True

    def update(self):
        if self.playing:
            if self.lastframetime + self.tbf < time.time():
                self.lastframetime = time.time()
                self.frame += 1
            self.img = self.frames[self.frame - 1]

    def draw(self, surf, coords):
        surf.blit(self.img, coords)


# Entity class, this is every object in the game,
# It can manage movement and collisions with other entites
class Entity:
    def collidecheck(self, rect, tiles):
        hitlist = []
        for tile in tiles:
            if rect.colliderect(tile):
                hitlist.append(tile)
        return hitlist

    def __init__(self, x, y, width, height):
        self.hitbox = pygame.Rect(x, y, width, height)
        self.touching = []
        self.isonground = False
        self.isonwall = False

    def move(self, motion, tiles):
        self.touching = []
        self.hitbox.x += motion[0]
        self.touching = self.collidecheck(self.hitbox, tiles)
        self.isonground = False
        self.isonwall = False

        for tile in self.touching:
            if motion[0] > 0:
                self.hitbox.right = tile.left
                self.isonwall = True
            if motion[0] < 0:
                self.hitbox.left = tile.right
                self.isonwall = True
        self.touching = []
        self.hitbox.y += motion[1]
        self.touching = self.collidecheck(self.hitbox, tiles)
        for tile in self.touching:
            if motion[1] > 0:
                self.hitbox.bottom = tile.top
                self.isonground = True
            if motion[1] < 0:
                self.hitbox.top = tile.bottom

        return motion

    def update(self):
        pass
