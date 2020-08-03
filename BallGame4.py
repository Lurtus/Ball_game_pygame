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
    
    def __init__(self, coords,radius, nbr):
        super(Ball,self).__init__()
        self.surf = pygame.Surface([2*radius,2*radius])
        self.surf.fill([255,255,255])
        self.surf.set_colorkey([255,255,255], RLEACCEL) #Masks the white color. #which color is transparent. RLEACCEL optional, faster rendering on non-acclerated displays
        
        self.radius = radius
        self.rect = self.surf.get_rect(center = coords)
        self.coords = np.array(self.rect)        
        self.mass = 1
        
        #self.speed = random.randint(5,20)
        self.speed = 5
        theta = random.uniform(0,np.pi*2)
                
#        if nbr == 0:
#            theta = 0
#        else:
#            theta = np.pi/2
        
        self.veldir = np.array([np.cos(theta), np.sin(theta)])
        
        self.nbr = nbr
        
    def update(self):
       

        vel = np.round(self.speed*self.veldir)
        self.rect.move_ip(vel) #Kanske blir avrundingsfel här? Bollar hamnar utanför skärmen ibland.
        
        self.coords = np.round(np.array([self.rect[0]+(self.radius+1)/2, self.rect[1]+(self.radius+1)/2])) #Plus 1 or not on radius?
        
        #self.coords = self.coords + vel

        if self.coords[0]-self.radius < 0 or self.coords[0]+self.radius >= SCREEN_WIDTH:
            self.veldir[0] = -self.veldir[0]     

        if self.coords[1]-self.radius < 0 or self.coords[1]+self.radius >= SCREEN_HEIGHT:
            self.veldir[1] = -self.veldir[1]
                
        self.surf.fill([255,255,255])        
        pygame.draw.circle(self.surf, [0,0,255],[self.radius,self.radius], self.radius)


#Function which computes the new velocities of two balls after collision
#Not to self, should be possible to generalize if multiple collisions occurs simultanously.
#Only works for m1=m2 and when d = 0 for some reason. (This case is quite easy to implement by cheating...)
def collision(ball1, ball2,d):
    
    #Find collision vector, defined from center of ball2 to collision point
    coll_dir = (ball2.coords-ball1.coords) 
    coll_dir = coll_dir/(np.sqrt(coll_dir[0]**2+coll_dir[1]**2))    
    
    #Solve second degree equation to compute magnitude of collision force
    v1 = np.round(ball1.speed*ball1.veldir)
    v2 = np.round(ball2.speed*ball2.veldir)

    relv = v2-v1
    speed_relv = np.sqrt(relv[0]**2+relv[1]**2)
    
    m1 = ball1.mass
    m2 = ball2.mass
    
    di = speed_relv*d/ ( (m1**2+m2**2)/(2*m1) )
    
    sp1 = v1[0]*coll_dir[0]+v1[1]*coll_dir[1]
    sp2 = -v2[0]*coll_dir[0]-v2[1]*coll_dir[1]
    
    p = 2*m1*m2/(m1**2+m2**2)*(sp1 + sp2)
    
    per = 2
    if di > 0.25*p**2:
        di = 0.25*p**2 - per
#        pdb.set_trace()
        
    
    
    k1 = -p/2 + 0.5*np.sqrt(p**2-4*di)
    k2 = -p/2 - 0.5*np.sqrt(p**2-4*di)
    
    
    if p < 0.0:
        k = k1  
    else:
        k = k2
    v1_new = v1+k*coll_dir
    v2_new = v2-k*coll_dir*m2/m1
    
#    v1_new = np.round(v1_new)
#    v2_new = np.round(v2_new)
    
#
 
    
    
    #Algorithm to perserve kinetic energy due to round off error
    speed1_b = np.sqrt(v1[0]**2+v1[1]**2)
    speed2_b = np.sqrt(v2[0]**2+v2[1]**2)
    K_b = 0.5*m1*speed1_b**2 + 0.5*m2*speed2_b**2
    
    
    speed1_a = np.sqrt(v1_new[0]**2+v1_new[1]**2)
    speed2_a = np.sqrt(v2_new[0]**2+v2_new[1]**2)
    
    K_a = 0.5*m1*speed1_a**2 + 0.5*m2*speed2_a**2
    
#    print(K_a)
#    print(K_b)
    
#    if abs(K_a -K_b - di) > 1:
#        print(K_a)
#        print(K_b)
#        pdb.set_trace()
    
    
#    print(k1)
#    print(k2)
#    print(k)
#    print('----------')
    #pdb.set_trace()
    #Update the velocities of ball1 and ball2
    #I should not alter the attributes directly, but rather define set and get commands...

    


#    v1_new_k1 = v1+k1*coll_dir
#    v2_new_k1 = v2-k1*coll_dir*m1/m2
#
#    v1_new_k2 = v1+k2*coll_dir
#    v2_new_k2 = v2-k2*coll_dir*m1/m2
#
#    speed1 = np.sqrt(v1[0]**2+v1[1]**2)
#    speed2 = np.sqrt(v2[0]**2+v2[1]**2)
#
#
#    speed1_k1 = np.sqrt(v1_new_k1[0]**2+v1_new_k1[1]**2)
#    speed2_k1 = np.sqrt(v2_new_k1[0]**2+v2_new_k1[1]**2)
#
#    speed1_k2 = np.sqrt(v1_new_k2[0]**2+v1_new_k2[1]**2)
#    speed2_k2 = np.sqrt(v2_new_k2[0]**2+v2_new_k2[1]**2)
#
#    if speed1_k1 < speed1:
#        v1_new = v1_new_k1
#    elif speed1_k2 < speed1 :
#        v1_new = v1_new_k2
#    else:
#        print(speed1)
#        print(speed1_k1)
#        print(speed1_k2)
#        
#        if speed1_k1 < speed1_k2:
#            v1_new = v1_new_k1
#        else:
#            v1_new = v1_new_k2
#        
##        pdb.set_trace()
#
#    if speed2_k1 < speed2:
#        v2_new = v2_new_k1
#    elif speed2_k2 < speed2:
#        v2_new = v2_new_k2
#    else:
#        print(speed2)
#        print(speed2_k1)
#        print(speed2_k2)
#        
#        if speed1_k1 < speed1_k2:
#            v2_new = v1_new_k1
#        else:
#            v2_new = v1_new_k2
        
        #pdb.set_trace()
#    print(speed1)
#    print(speed2)


    ball1.speed = np.sqrt(v1_new[0]**2 + v1_new[1]**2 ) #Should be conserved when d = 0
    ball2.speed = np.sqrt(v2_new[0]**2 + v2_new[1]**2 ) # should be conserved when d = 0
    
    print(ball1.speed)
    print(ball2.speed)
    #Could actually be due to round off errors and the pixel size approach?
    
    ball1.veldir = v1_new/ball1.speed
    ball2.veldir = v2_new/ball2.speed    
    
    #Positions should be updated such that new position is outside the balls 
    #(what if this position collides whith another ball?) This will also increase the speed momentarily...
    
#    print(k1)
#    print(k2)
#    print(p)
#    print(k)
#    pdb.set_trace()
    print('--------')
#    tm.sleep(10)
    #pdb.set_trace()
    
#Main game:

pygame.init()
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
pygame.display.set_caption('Ball Game')

balls = pygame.sprite.Group()

clock = pygame.time.Clock()
running = True

coll_dissipation = 0
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
            new_ball = Ball(coords, radius,nbr)
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
    
    print(totK)
    
    balls.update()

    
    pygame.display.flip()
    clock.tick(100)