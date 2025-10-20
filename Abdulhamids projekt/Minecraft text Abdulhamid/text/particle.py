import pygame
import random
import math

class Particle:
    def __init__(self, effect, x, y, color):
        self.effect = effect
        self.x = random.randint(0, self.effect.width)
        self.y = self.effect.height
        self.originX = x
        self.originY = y
        self.size = self.effect.gap
        self.color = color
        self.dx = 0
        self.dy = 0
        self.vx = 0
        self.vy = 0
        self.force = 0
        self.angle = 0
        self.distance = 0
        self.friction = random.random() * 0.6 + 0.15
        self.ease = random.random() * 0.1 + 0.005

    def update(self, mouse_x, mouse_y):
        self.dx = mouse_x - self.x
        self.dy = mouse_y - self.y
        self.distance = self.dx * self.dx + self.dy * self.dy
        self.force = -self.effect.mouse_radius / self.distance 

        if self.distance < self.effect.mouse_radius:
            self.angle = math.atan2(self.dy, self.dx)
            self.vx += self.force * math.cos(self.angle)
            self.vy += self.force * math.sin(self.angle)
        
        self.vx = self.vx*self.friction
        self.vy = self.vy*self.friction

        self.x += (self.vx) + (self.originX - self.x) * self.ease
        self.y += (self.vy) + (self.originY - self.y) * self.ease

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.size, self.size))

