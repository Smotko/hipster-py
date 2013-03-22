import pygame, sys, os, time
from pygame.locals import *
from pygame.time import Clock
from random import random

# INIT:

pygame.init()

clock = Clock()

WIDTH  = 640
HEIGHT = 480 

window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pygame!")
screen = pygame.display.get_surface()

PLAYER_MOVE_FACTOR = .4
ENEMY_MOVE_FACTOR  = .2
# SPRITES:

hipster_path = os.path.join("assets", "hipster.png")
hipster_surface = pygame.image.load(hipster_path)
hipster_pos = [WIDTH/2-64,-128]

superman_path  = os.path.join("assets", "superman.png")
superman_surface = pygame.image.load(superman_path)
superman_pos = [WIDTH/2,HEIGHT/2]
superman_dir = [0,0]

background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill((250, 250, 250))

# INPUT:

def input_key_down(key):
    if key == K_ESCAPE: 
        sys.exit(0)
    for i,k in enumerate([K_LEFT, K_UP, K_RIGHT, K_DOWN]):
        if key == k:
            superman_dir[i%2] += 1 * (0.1+i-2)/abs(0.1+i-2)

def input_key_up(key):
    for i,k in enumerate([K_RIGHT, K_DOWN, K_LEFT, K_UP]):
        if key == k:
            superman_dir[i%2] += 1 * (0.1+i-2)/abs(0.1+i-2)
       
def input(events):
    for event in events:
        if event.type == QUIT:
            sys.exit(0)
        elif event.type == KEYUP:
            input_key_up(event.key)
        elif event.type == KEYDOWN:
            input_key_down(event.key)

def are_colliding():
    for i in [0,1]:
        if superman_pos[i]+64+34 < hipster_pos[i]+64-34 or \
           superman_pos[i]+64-34 > hipster_pos[i]+64+34:
            return False
    return True

# UPDATE: 
def update(delta):
    # move the hipster
    superman_pos[0] += superman_dir[0] * delta * PLAYER_MOVE_FACTOR
    superman_pos[1] += superman_dir[1] * delta * PLAYER_MOVE_FACTOR

    for i in [0,1]:    
        if superman_pos[i] < 0:
            superman_pos[i] = 0

    for i,s in enumerate([WIDTH, HEIGHT]):
        if superman_pos[i] > s-128:
            superman_pos[i] = s-128

    hipster_pos[1] += delta * ENEMY_MOVE_FACTOR

    
    if hipster_pos[1] > HEIGHT + 128 or are_colliding():
        hipster_pos[0] = random()*(WIDTH-128)
        hipster_pos[1] = -128

    

# DRAW: 


def draw():
    screen.blit(background, (0,0))
    screen.blit(hipster_surface, hipster_pos)
    screen.blit(superman_surface, superman_pos)
    pygame.display.flip()

while True:
    input(pygame.event.get())
    update(clock.tick())
    draw()
