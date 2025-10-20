import pygame, sys
from pygame.locals import *
import time
import random
import math

pygame.init()

width=1365
height=688

window = pygame.display.set_mode((width,height), 0, 32)
pygame.display.set_caption('PyGame-Skelett')
clock = pygame.time.Clock()

class Nordicflag:
    def __init__(self, crosscolor, backgroundcolor):  # init-metoden anropas då ett nytt objekt skapas
        self.crosscolor = crosscolor                               #self står för ett unikt objekts egna data
        self.backgroundcolor = backgroundcolor
        self.yta = pygame.Surface((500, 200))
        self.vinkel = random.randint(0, 90)
        print(self.vinkel)
        
        

    def draw(self):
        self.yta.fill((255,255,255))
        pygame.draw.rect(self.yta, (self.backgroundcolor), pygame.Rect(0,0,500,200))
        pygame.draw.rect(self.yta, (self.crosscolor), pygame.Rect(250, 0, 60, 200))                     #Rita korset som två rektanglar med korsfärgen
        pygame.draw.rect(self.yta, (self.crosscolor), pygame.Rect(0, 100, 500, 60))
        
        roterad = pygame.transform.rotate(self.yta, self.vinkel)
        window.blit(roterad, (0,0))

danskflagga = Nordicflag((255,255,255),(255,0,0)) #Vitt kors och röd bakgrund

while True:

 clock.tick (60)
 for event in pygame.event.get():
   if event.type == QUIT:
      pygame.quit()
      sys.exit()
 window.fill((255,255,255))
 danskflagga.draw()
 pygame.display.update()
