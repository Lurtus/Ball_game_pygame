#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 30 22:17:41 2020

@author: eric
"""

import pygame
import pdb
import random
import numpy as np

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

from pygame.locals import (
        RLEACCEL,
        MOUSEBUTTONDOWN,
        MOUSEBUTTONUP,
        QUIT,
)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
radius = 25


#Classess:
class Ball(pygame.sprite.Sprite):
    
    def __init__(self, coords,radius):
        super(Ball,self).__init__()
        self.surf = pygame.Surface([2*radius,2*radius])
        self.surf.fill([255,255,255])
        self.surf.set_colorkey([255,255,255], RLEACCEL) #Masks the white color. #which color is transparent. RLEACCEL optional, faster rendering on non-acclerated displays
        
        self.coords = coords
        self.radius = radius
        self.rect = self.surf.get_rect(center = coords)
        
        self.speed = random.randint(5,20)
        theta = random.uniform(0,np.pi*2)
        self.veldir = np.array([np.cos(theta), np.sin(theta)])
        
    def update(self):
       

        vel = self.speed*self.veldir
        self.rect.move_ip(vel)
        self.coords = self.coords + vel

        if self.coords[0]-self.radius < 0 or self.coords[0]+self.radius >= SCREEN_WIDTH:
            self.veldir[0] = -self.veldir[0]     

        if self.coords[1]-self.radius < 0 or self.coords[1]+self.radius >= SCREEN_HEIGHT:
            self.veldir[1] = -self.veldir[1]
                
        self.surf.fill([255,255,255])        
        pygame.draw.circle(self.surf, [0,0,255],[self.radius,self.radius], self.radius)
        

#Main game:

pygame.init()
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

balls = pygame.sprite.Group()

clock = pygame.time.Clock()
running = True

while running:
        
    
    screen.fill([255,255,255])  
    
    for event in pygame.event.get():
        
        if event.type == QUIT:
            running = False
            
        elif event.type == MOUSEBUTTONDOWN:
            coords = np.array(pygame.mouse.get_pos())
            #print(coords)
            #pygame.draw.circle(screen, [0,0,255], coords, 25)
            new_ball = Ball(coords, radius)
            balls.add(new_ball)


    for ball in balls:
        screen.blit(ball.surf,ball.rect)
        
        if len(balls) > 1:
            other_balls = balls.copy()
            other_balls.remove(ball)
        
            for other_ball in other_balls:
                if pygame.sprite.collide_circle(ball,other_ball): #Can not use groups with this one?
                    ball.speed = 0
        
            #if pygame.sprite.spritecollideany(ball, other_balls):
            #    ball.speed = 0
    
    
  
    balls.update()

    
    pygame.display.flip()
    clock.tick(30)