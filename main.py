import pygame
import neat
import time
import os
import random

WIN_WIDTH = 600
WIN_HEIGHT = 800

BIRD_IMGS = [
    pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird1.png"))),
    pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird2.png"))),
    pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird3.png")))
]
PIPE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "pipe.png")))
BASE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "base.png")))
BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bg.png")))

class Bird:
    IMGS = BIRD_IMGS
    MAX_ROTATION = 25
    ROT_VEL = 20
    ANIMATION_TIME = 5

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tilt = 0
        self.tick_count = 0
        self.vel = 0
        self.height = self.y
        self.img_count = 0
        self.img = self.IMGS[0]\



    def jump(self):
        self.vel = -10.5 # negative velocity means go up
        self.tick_count = 0 # time
        self.height = self.y 



    def move(self):
        self.tick_count += 1
        # displacement = velocity * time + 1.5 * acceleration * time^2
        d = self.vel * self.tick_count + 1.5 * self.tick_count ** 2 # accelleration

        if d >= 16: # terminal velocity
            d = 16

        if d < 0: # fine tuning jump height
            d -= 2 

        self.y += d # makes the birds y position change to be equal to d 

        if d < 0 or self.y < self.height + 50: # 0 is the middle of the screen
            if self.tilt < self.MAX_ROTATION: # if too much tilt,       (this is for jumping)
                self.tilt = self.MAX_ROTATION # turn it down to max tilt
        else:
            if self.tilt > -90: # make it so the bird 
                self.tilt -= self.ROT_VEL #  can nosedive 
    


    def draw(self, win): # draw the bird with animations
        self.img_count += 1 # count the number of times the bird has been drawn

        if self.img_count < self.ANIMATION_TIME:
            self.img = self.IMGS[0]
        elif self.img_count < self.ANIMATION_TIME * 2:
            self.img = self.IMGS[1]
        elif self.img_count < self.ANIMATION_TIME * 3:
            self.img = self.IMGS[2]
        elif self.img_count < self.ANIMATION_TIME * 4:
            self.img = self.IMGS[1]
        elif self.img_count == self.ANIMATION_TIME * 4 + 1:
            self.img = self.IMGS[0]
            self.img_count = 0

        if self.tilt <= -80: # if the bird is nosediving 
            self.img = self.IMGS[1] # make the wings not flap
            self.img_count = self.ANIMATION_TIME * 2 # prevents skipping frame when nosediving stops

        rotated_image = pygame.transform.rotate(self.img, self.tilt) # rotate the bird
        new_rect = rotated_image.get_rect(center=self.img.get_rect(topleft = (self.x, self.y)).center) # get the center of the bird to rotate around
        win.blit(rotated_image, new_rect.topleft) 

    

    def get_mask(self):
        return pygame.mask.from_surface(self.img)