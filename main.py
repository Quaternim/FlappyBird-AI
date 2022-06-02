from audioop import add
import re
import pygame
import neat
import time
import os
import random

pygame.font.init()  # init font

# fix my code


WIN_WIDTH = 550
WIN_HEIGHT = 800

BIRD_IMGS = [
    pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird1.png"))),
    pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird2.png"))),
    pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird3.png")))
]
PIPE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "pipe.png")))
BASE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "base.png")))
BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bg.png")))

STAT_FONT = pygame.font.SysFont("arial", 50)

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
        win.blit(rotated_image, new_rect.topleft)  # i think blit means draw in pygame

    

    def get_mask(self):
        return pygame.mask.from_surface(self.img) # mask for pixel perfect collision




class Pipe:
    GAP = 200 # gap between the pipes
    VEL = 5 # speed the pipes move towards the bird

    def __init__(self, x):
        self.x = x # self-explanatory
        self.height = 0 # self-explanatory

        self.top = 0
        self.bottom = 0
        self.PIPE_TOP = pygame.transform.flip(PIPE_IMG, False, True) # the pipe is just one image so it needs to be flipped for the top pipe
        self.PIPE_BOTTOM = PIPE_IMG

        self.passed = False # if the bird has passed the pipe
        self.set_height()

    def set_height(self):
        self.height = random.randrange(50, 450)
        self.top = self.height - self.PIPE_TOP.get_height()
        self.bottom = self.height + self.GAP

    def move(self):
        self.x -= self.VEL # move the pipe towards the bird (left)

    def draw(self, win):
        win.blit(self.PIPE_TOP, (self.x, self.top))
        win.blit(self.PIPE_BOTTOM, (self.x, self.bottom))

    def collide(self, bird):
        bird_mask = bird.get_mask() # get the bird's mask
        top_mask = pygame.mask.from_surface(self.PIPE_TOP) # get the top pipe's mask
        bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM) # get the bottom pipe's mask

        top_offset = (self.x - bird.x, self.top - round(bird.y)) # get the offset of the top pipe
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y)) # get the offset of the bottom pipe

        b_point = bird_mask.overlap(bottom_mask, bottom_offset) # get the point of overlap between the bird and the bottom pipe
        t_point = bird_mask.overlap(top_mask, top_offset) # get the point of overlap between the bird and the top pipe

        if t_point or b_point:
            return True
        
        return False


class Base:
    VEL = 5
    WIDTH = BASE_IMG.get_width()
    IMG = BASE_IMG

    def __init__(self, y):
        self.y = y
        self.x1 = 0 # dont need explaining
        self.x2 = self.WIDTH

    def move(self):
        self.x1 -= self.VEL # make move
        self.x2 -= self.VEL # make move

        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH
        # if the second base is off the screen, make it the first base
        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH

    def draw(self, win):
        win.blit(self.IMG, (self.x1, self.y))
        win.blit(self.IMG, (self.x2, self.y))
        



def draw_window(win, bird, pipes, base, score):
    win.blit(BG_IMG, (0,0))

    for pipe in pipes:
        pipe.draw(win)

    text = STAT_FONT.render("Score: " + str(score), 1, (255,255,255))
    win.blit(text, (WIN_WIDTH - 10 - text.get_width(), 10))

    base.draw(win)

    bird.draw(win)
    pygame.display.update()




def main():
    bird = Bird(230, 350)
    base = Base(730)
    pipes = [Pipe(600)]
    score = 0


    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    clock = pygame.time.Clock()


    run = True
    while run:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # bird.move()
        
        add_pipe = False
        rem = []
        for pipe in pipes:
            if pipe.collide(bird):
                pass

            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                rem.append(pipe)

            if not pipe.passed and pipe.x < bird.x: 
                pipe.passed = True
                add_pipe = True

            pipe.move()
    
        if add_pipe:
            score += 1
            pipes.append(Pipe(600))

        for r in rem:
            pipes.remove(r)
        
        if bird.y + bird.img.get_height() >= 730:
            pass


        base.move()
        draw_window(win, bird, pipes, base, score)
    pygame.quit()
    quit()

main()

