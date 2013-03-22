import pygame, sys, os, time
from pygame.locals import *
from pygame.time import Clock
from random import random

# INIT:

pygame.init()

clock = Clock()

WIDTH  = 640
HEIGHT = 480 

score = 0
game_state = 'GAME'

window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hipster Py")
screen = pygame.display.get_surface()

PLAYER_MOVE_FACTOR = 1
ENEMY_MOVE_FACTOR  = 0.6

# SPRITES:

background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill((250, 250, 250))

font = pygame.font.Font(None, 36)
class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, filename, num_anims, fps = 10):
        pygame.sprite.Sprite.__init__(self)
        
        self._images = self._create_images(filename, num_anims)
        self._start = pygame.time.get_ticks()
        self._delay = 1000 / fps
        self._last_frame  = 0
        self._frame = 0
        self._acum = 0

        self.rect = self._images[0].get_rect()
        self.direction = [0,0]
        # Call update to set our first image.
        self.update(pygame.time.get_ticks())

    def update(self, t):
        self._acum += t
        if self._acum > self._delay:
            self._frame += 1
            self._frame %= len(self._images)
            self.image = self._images[self._frame]
            self._acum = 0

    def _create_images(self, filename, num_anims):
        image = pygame.image.load(os.path.join('assets', filename)).convert_alpha()
    
        w, h = image.get_size()
        return [image.subsurface((i*h, 0, h, h)) for i in xrange(num_anims)]

class HipsterSprite(AnimatedSprite):
    def update(self, delta):
        AnimatedSprite.update(self, delta)
        
        self.rect.centery += delta * ENEMY_MOVE_FACTOR

        if self.rect.top > HEIGHT: 
            pass

        if self.rect.colliderect(superman.rect.inflate(-128, -128)):
            global score
            score += 1
            explosion.rect.center = self.rect.center
            self.rect.left = random()*(WIDTH-self.rect.width)
            self.rect.bottom = 0

class SupermanSprite(AnimatedSprite):
    
    def update(self, delta):
        AnimatedSprite.update(self, delta)
        self.rect.centerx += self.direction[0] * delta
        self.rect.centery += self.direction[1] * delta
        
            
explosion = AnimatedSprite("explosion.png", 7)
explosion.rect.center = (-100, -100)
superman = SupermanSprite("superman.png", 1)
superman.rect.midbottom = (WIDTH/2, HEIGHT)
hipster = HipsterSprite("hipster.png", 3)
all_sprites = pygame.sprite.RenderPlain((explosion,hipster,superman))

# INPUT:

def input_key_down(key):
    if key == K_ESCAPE: 
        sys.exit(0)
    for i,k in enumerate([K_LEFT, K_UP, K_RIGHT, K_DOWN]):
        if key == k:
            superman.direction[i%2] += 1 * (0.1+i-2)/abs(0.1+i-2)

def input_key_up(key):
    for i,k in enumerate([K_RIGHT, K_DOWN, K_LEFT, K_UP]):
        if key == k:
            superman.direction[i%2] += 1 * (0.1+i-2)/abs(0.1+i-2)
       
def input(events):
    for event in events:
        if event.type == QUIT:
            sys.exit(0)
        elif event.type == KEYUP:
            input_key_up(event.key)
        elif event.type == KEYDOWN:
            input_key_down(event.key)

def draw_menu():
    font = pygame.font.Font(None, 42)
    text = font.render("Hipster py", 1, (10, 10, 10))
    textpos = text.get_rect()
    textpos.centerx = background.get_rect().centerx
    textpos.centery = background.get_rect().centery
    screen.blit(text, textpos)

def draw_score():
    font = pygame.font.Font(None, 42)
    text = font.render(str(score), 1, (10, 10, 10))
    textpos = text.get_rect()
    textpos.centerx = background.get_rect().centerx
    screen.blit(text, textpos)
    

def draw():
    screen.blit(background, (0,0))
    draw_score()
    print game_state
    if game_state == 'GAME':
        all_sprites.draw(screen)
    if game_state == 'MENU':
        draw_menu()

    screen.blit(background, (0,0))
    pygame.display.flip()

# GAME LOOP
while True:
    input(pygame.event.get())
    all_sprites.update(clock.tick())
    draw()
