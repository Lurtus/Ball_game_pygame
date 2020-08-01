#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 30 22:17:41 2020

@author: eric
"""

import pygame
import pdb
import random


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
        self.surf = pygame.Surface([radius,radius])
        self.surf.fill([255,255,255])
        self.coords = coords
        self.radius = radius
        self.rect = self.surf.get_rect()


    def update(self):
        pygame.draw.circle(screen, [0,0,255], self.coords, self.radius)

#Main game:

pygame.init()
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

balls = pygame.sprite.Group()

clock = pygame.time.Clock()
running = True

while running:
        
    for event in pygame.event.get():
        
        if event.type == QUIT:
            running = False
            
        elif event.type == MOUSEBUTTONDOWN:
            coords = pygame.mouse.get_pos()
            
            #print(coords)
            #pygame.draw.circle(screen, [0,0,255], coords, 25)
            new_ball = Ball(coords, radius)
            balls.add(new_ball)

    screen.fill([255,255,255])    
    balls.update()    

    
    for ball in balls:
        screen.blit(ball.surf,ball.rect)
    
    pygame.display.flip()
    clock.tick(30)