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
import time as tm

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
    
    def __init__(self, coords, nbr):
        super(Ball,self).__init__()
  
        
        self.radius = random.randint(10,40)
        
        #self.radius = 25
        self.mass = self.radius
        
        self.surf = pygame.Surface([2*self.radius,2*self.radius])
        self.surf.fill([255,255,255])
        self.surf.set_colorkey([255,255,255], RLEACCEL) #Masks the white color. #which color is transparent. RLEACCEL optional, faster rendering on non-acclerated displays
        
        self.rect = self.surf.get_rect(center = coords)
        self.coords = coords      
        
        self.speed = random.randint(5,15)

        theta = random.uniform(0,np.pi*2)        
        self.veldir = np.array([np.cos(theta), np.sin(theta)])        

        self.nbr = nbr
        
    def update(self):
       
        vel = self.speed*self.veldir
        self.coords = self.coords + vel
        self.rect.move_ip([self.coords[0]-self.rect.x,self.coords[1]-self.rect.y   ])

        if self.coords[0]-self.radius < 0 or self.coords[0]+self.radius >= SCREEN_WIDTH:
            self.veldir[0] = -self.veldir[0]     

        if self.coords[1]-self.radius < 0 or self.coords[1]+self.radius >= SCREEN_HEIGHT:
            self.veldir[1] = -self.veldir[1]

        self.surf.fill([255,255,255]) 
        pygame.draw.circle(self.surf, [0,0,255],[self.radius,self.radius], self.radius)


#Function which computes the new velocities of two balls after collision
#Not to self, should be possible to generalize if multiple collisions occurs simultanously.
def collision(ball1, ball2,d):
    
    #Find collision vector, defined from center of ball2 to collision point

    coll_dir = (ball2.coords-ball1.coords) 
    
    coll_dir = coll_dir/(np.sqrt(coll_dir[0]**2+coll_dir[1]**2))    
    
    #Solve second degree equation to compute magnitude of collision force
    v1 = ball1.speed*ball1.veldir
    v2 = ball2.speed*ball2.veldir

    relv = v2-v1
    speed_relv = np.sqrt(relv[0]**2+relv[1]**2)
    
    m1 = ball1.mass
    m2 = ball2.mass
    
    di = (m1+m2)*speed_relv*d*( 2*m1/(m1*m2+m2**2)) 
    
    sp1 = v1[0]*coll_dir[0]+v1[1]*coll_dir[1]
    sp2 = -v2[0]*coll_dir[0]-v2[1]*coll_dir[1]
    
    p = 2*m1/(m1+m2)*(sp1 + sp2)
    
    if di > 0.25*p**2: #To prevent complex roots. What does complex roots imply?
        di = (1-1e-6)*0.25*p**2
#        pdb.set_trace()
        
    k1 = -p/2 + 0.5*np.sqrt(p**2-4*di)
    k2 = -p/2 - 0.5*np.sqrt(p**2-4*di)

    if p < 0.0:
        k = k1  
    else:
        k = k2
        
    
    v1_new = v1+k*coll_dir
    v2_new = v2-k*coll_dir*m2/m1
    
    ball1.speed = np.sqrt(v1_new[0]**2 + v1_new[1]**2 ) 
    ball2.speed = np.sqrt(v2_new[0]**2 + v2_new[1]**2 )
        
    ball1.veldir = v1_new/ball1.speed
    ball2.veldir = v2_new/ball2.speed    
        
    
#Main game:

pygame.init()
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
pygame.display.set_caption('Ball Game')

balls = pygame.sprite.Group()

clock = pygame.time.Clock()
running = True

coll_dissipation = 10
nbr = 0

coll_prevframe = [] #list of integers keeping track if balls were colliding in previous frame or not.


while running:
        
    
    screen.fill([255,255,255])  
    
    for event in pygame.event.get():
        
        if event.type == QUIT:
            running = False
            
        elif event.type == MOUSEBUTTONDOWN:
            coords = np.array(pygame.mouse.get_pos())
            #print(coords)
            #pygame.draw.circle(screen, [0,0,255], coords, 25)
            
            new_ball = Ball(coords,nbr)
            balls.add(new_ball)
            nbr +=1

    
    other_balls = balls.copy()
    
    totK = 0
    
    for ball in balls:
        screen.blit(ball.surf,ball.rect)
        
        if len(other_balls) > 1:
            
            other_balls.remove(ball)
        
            for other_ball in other_balls:
                i = ball.nbr
                j = other_ball.nbr
                
                if pygame.sprite.collide_circle(ball,other_ball): #Can not use groups with this one?                    
                    if [i,j] not in coll_prevframe:    
                        collision(ball,other_ball,coll_dissipation) 
                        coll_prevframe.append([i,j])
                        

                else:
                    if [i,j] in coll_prevframe:
                        coll_prevframe.remove([i,j])
        
        totK += 0.5*ball.mass*ball.speed**2
    
    #print(totK)
    
    balls.update()

    
    pygame.display.flip()
    clock.tick(40)