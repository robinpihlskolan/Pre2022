import pygame
from settings import *

class Platform:
    def __init__(self, x, y, type="normal"):
        self.width = Platform_WIDTH
        self.height = Platform_HEIGHT
        self.x = x
        self.y = y
        self.type = type
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.moving_right = True
        self.speed = 2 if type == "moving" else 0
    
    def update (self):
        if self.type== "moving":
            if self.moving_right:
                self.x +=self.speed
                if self.x+self.width >=WIDTH:
                    self.moving_right=False
            
            else:
                self.x-=self.speed
                if self.x<=0:
                    self.moving_right=True
            self.rect.x=self.x
    def draw(self,screen):
        if self.type == "normal":
            pygame.draw.rect(screen,GREEN,self.rect)
        elif self.type== "moving":
            pygame.draw.rect(screen,BLUE, self.rect)
        elif self.type== "breaking":
            pygame.draw.rect(screen,RED, self.rect)
        elif self.type =="spring" :
            pygame.draw.rect(screen,GREEN,self.rect)
            spring_x = self.x + self.width // 2 - 5
            pygame.draw.rect(screen, RED, (spring_x, self.y - 10, 10, 10))
