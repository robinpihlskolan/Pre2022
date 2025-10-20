import pygame
from settings import *

class PowerUp:
    def __init__(self,x,y,type="jetpack"):
        self.x=x
        self.y=y
        self.type=type
        self.width= Powerup_WIDTH
        self.height=Powerup_HEIGHT
        self.rect=pygame.Rect(x,y,self.width,self.height)
    def draw(self,screen):
        if self.type =="jetpack":
            pygame.draw.rect(screen,RED,self.rect)