import pygame
from Code.scripts.engine.FrameWork import *


class Player:
    def __init__(self):
        self.Direction = {"Up": False,"Down": False, "Left": False,"Right": False}
        self.Hitbox = pygame.Rect(0, 0, 16, 22)
        self.vel = pygame.Vector2(0, 0)
        self.direction = "IdleDown"
        self.animations = {"IdleLeft" : Animation([load_img("Code/resources/Assets/PlayerWalkCycle/WalkCycleCharacterTemplate7.png")], .1), "IdleRight" : Animation([load_img("Code/resources/Assets/PlayerWalkCycle/WalkCycleCharacterTemplate1.png")], .1), "IdleUp" : Animation([load_img("Code/resources/Assets/PlayerWalkCycle/WalkCycleCharacterTemplate19.png")], .1), "IdleDown" : Animation([load_img("Code/resources/Assets/PlayerWalkCycle/WalkCycleCharacterTemplate13.png")], .1)}
    def Event(self, event):
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w or event.key == pygame.K_UP:
                self.Direction["Up"] = False

            if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                self.Direction["Down"] = False

            if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                self.Direction["Left"] = False

            if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                self.Direction["Right"] = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w or event.key == pygame.K_UP:
                self.Direction["Up"] = True

            if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                self.Direction["Down"] = True

            if event.key == pygame.K_a  or event.key == pygame.K_LEFT:
                self.Direction["Left"] = True

            if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                self.Direction["Right"] = True
    def Update(self):

        if self.Direction["Up"]:
            self.direction = "IdleUp"
            self.Hitbox.y -= 1

        if self.Direction["Down"]:
            self.direction = "IdleDown"
            self.Hitbox.y += 1

        if self.Direction["Left"]:
            self.direction = "IdleLeft"
            self.Hitbox.x += -1

        if self.Direction["Right"]:
            self.direction = "IdleRight"
            self.Hitbox.x += 1

    def Draw(self, screen):

        screen.blit(self.animations[self.direction].img, (self.Hitbox.x, self.Hitbox.y))