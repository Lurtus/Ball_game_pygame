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
import thorpy

SCREEN_WIDTH = 900
SCREEN_HEIGHT = 700
PLAYCREEN_HEIGHT = SCREEN_HEIGHT-100

from pygame.locals import (
        RLEACCEL,
        MOUSEBUTTONDOWN,
        MOUSEBUTTONUP,
        QUIT,
)


#Classess:
class Ball(pygame.sprite.Sprite):
    
    def __init__(self, coords, veldir,speed, nbr, radius):
        super(Ball,self).__init__()
  
        
        #self.radius = random.randint(10,40)        
        self.radius = radius
        self.mass = self.radius**2        
        self.surf = pygame.Surface([2*self.radius,2*self.radius])
        self.surf.fill([255,255,255])
        #self.surf.set_colorkey([255,255,255], RLEACCEL) #Masks the white color. #which color is transparent. RLEACCEL optional, faster rendering on non-acclerated displays
        self.surf.set_colorkey([255,255,255])
        
        self.rect = self.surf.get_rect(center = coords)
        self.coords = coords     #This one refers to top left point of surf! (even when I used center above...) 
        
#        self.speed = random.randint(5,15)
#        theta = random.uniform(0,np.pi*2)        
#        self.veldir = np.array([np.cos(theta), np.sin(theta)])        

        self.speed = speed        
        self.veldir = veldir       

        self.nbr = nbr
        
    def update(self):

        if self.speed < 0.5:
            self.speed = 0
        
        vel = self.speed*self.veldir
        self.coords = self.coords + vel
        self.rect.move_ip([ int(np.round(self.coords[0]-self.rect.x)),int(np.round(self.coords[1]-self.rect.y)  ) ])

        if self.coords[0] < 0:
            self.veldir[0] = np.abs(self.veldir[0])
            
        if self.coords[0]+self.radius*2 >= SCREEN_WIDTH:
            self.veldir[0] = -np.abs(self.veldir[0])   
        
        if self.coords[1] < 0:
            self.veldir[1] = np.abs(self.veldir[1])
            
        if self.coords[1]+self.radius*2 >= PLAYCREEN_HEIGHT:
            self.veldir[1] = -np.abs(self.veldir[1])
            
        self.surf.fill([255,255,255]) 
        pygame.draw.circle(self.surf, [0,0,255],[self.radius,self.radius], self.radius)


#Function which computes the new velocities of two balls after collision
#Not to self, should be possible to generalize if multiple collisions occurs simultanously.
def collision(ball1, ball2,d):
    
    #Find collision vector, defined from center of ball2 to collision point

    coll_dir = (ball2.coords-ball1.coords) + [ball2.radius-ball1.radius,ball2.radius-ball1.radius] #Need to add this part to get to center of ball
    coll_dir = coll_dir/(np.sqrt(coll_dir[0]**2+coll_dir[1]**2))    
    
    #Solve second degree equation to compute magnitude of collision force
    v1 = ball1.speed*ball1.veldir
    v2 = ball2.speed*ball2.veldir

    relv = v2-v1
    speed_relv = np.sqrt(relv[0]**2+relv[1]**2)
    
    m1 = ball1.mass
    m2 = ball2.mass
    
    di = d*(m1+m2)*speed_relv*8/(m1*m2*(m1+m2))
    
    sp1 = v1[0]*coll_dir[0]+v1[1]*coll_dir[1]
    sp2 = -v2[0]*coll_dir[0]-v2[1]*coll_dir[1]
    
    p = 2/(m1+m2)*(sp1 + sp2)
    
    if di > p**2: #To prevent complex roots. What does complex roots imply?
        di = (1-1e-6)*p**2
#        pdb.set_trace()
        
    k1 = -p/2 + 0.5*np.sqrt(p**2-di)
    k2 = -p/2 - 0.5*np.sqrt(p**2-di)

    if p < 0.0:
        k = k1  
    else:
        k = k2
        
    
    v1_new = v1+k*m2*coll_dir
    v2_new = v2-k*m1*coll_dir
    
    ball1.speed = np.sqrt(v1_new[0]**2 + v1_new[1]**2 ) 
    ball2.speed = np.sqrt(v2_new[0]**2 + v2_new[1]**2 )
        
    ball1.veldir = v1_new/ball1.speed
    ball2.veldir = v2_new/ball2.speed    
    
#    print(p)
#    print(k1)
#    print(k2)
#    print(k)
    
#Main game:

pygame.init()
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
#screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption('Ball Game')

balls = pygame.sprite.Group()
clock = pygame.time.Clock()


massSlider = thorpy.SliderX(40, [10,50], 'Mass slider             ', type_=int)
massSlider.set_font_size(14)
quitButton = thorpy.make_button('Quit', func = thorpy.functions.quit_func)
quitButton.set_font_size(14)
box = thorpy.Box(elements=[massSlider,quitButton])

box.set_main_color([255,255,255])
box_xsize = 100
box_ysize = 5
box.enlarge([box_xsize,box_ysize])
menu = thorpy.Menu(box)

for element in menu.get_population():
    element.surface = screen
    
box.set_topleft([SCREEN_WIDTH/2-box_xsize,SCREEN_HEIGHT-(SCREEN_HEIGHT-PLAYCREEN_HEIGHT)+box_ysize])


thorpy.store(box, mode='h', align='bottom', gap=25)

box.blit()
box.update()

running = True

coll_dissipation = 100
nbr = 0

coll_prevframe = [] #list of integers keeping track if balls were colliding in previous frame or not.
mousedown = False
speed_init = 1

screen.fill([255,255,255])  
pygame.draw.line(screen, [0,0,0], [0,PLAYCREEN_HEIGHT], [SCREEN_WIDTH,PLAYCREEN_HEIGHT],2)


while running:
    
    screen.fill([255,255,255])  
    pygame.draw.line(screen, [0,0,0], [0,PLAYCREEN_HEIGHT], [SCREEN_WIDTH,PLAYCREEN_HEIGHT],2)
    
    for event in pygame.event.get():
        
        if event.type == QUIT:
            running = False
            
        elif event.type == MOUSEBUTTONDOWN and mousedown == False:
            coords = np.array(pygame.mouse.get_pos())
            
            if coords[1] < PLAYCREEN_HEIGHT:
                mousedown = True
                
        if event.type == MOUSEBUTTONUP and mousedown == True:
            
            new_ball = Ball(coords,veldir_init_ball,speed_init_ball, nbr,radius)
            balls.add(new_ball)
            nbr +=1
            mousedown = False
            
            
        menu.react(event)

    if mousedown == True:
        radius = massSlider.get_value()
        pygame.draw.circle(screen, [0,0,255], coords, radius)
    
        mousepos = np.array(pygame.mouse.get_pos())
        
        if mousepos[0] != coords[0] and mousepos[1] != coords[1]:
        
            veldir_init = mousepos-coords
            speed_init = np.sqrt(veldir_init[0]**2+veldir_init[1]**2)
        
            if speed_init < 100:
                pygame.draw.line(screen, [0,0,0], coords, mousepos,2)
                mousepos_old = mousepos
                #pygame.draw.circle(screen, [0,0,0], coords, speed_init, width=1)
            else:
                pygame.draw.line(screen, [0,0,0], coords, mousepos_old,2)
                veldir_init = mousepos_old-coords

                speed_init = np.sqrt(veldir_init[0]**2+veldir_init[1]**2)
    
            veldir_init_ball = veldir_init/speed_init
            speed_init_ball = speed_init/4
    
            if speed_init_ball < 4:
                speed_init_ball = 0
    
    
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
                    if ([i,j] or [j,i] ) not in coll_prevframe:    
                        collision(ball,other_ball,coll_dissipation) 
                        coll_prevframe.append([i,j])
                        coll_prevframe.append([j,i]) #Might be redundant. Not sure if it improves collision detection
                        

                else:
                    if [i,j] in coll_prevframe:
                        coll_prevframe.remove([i,j])
                        coll_prevframe.remove([j,i])
                        
        totK += 0.5*ball.mass*ball.speed**2
    
    
    #print(totK)
    
    balls.update()
    pygame.display.flip()
    menu.blit_and_update()
    clock.tick(40)