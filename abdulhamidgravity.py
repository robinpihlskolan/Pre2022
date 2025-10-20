import pygame
import sys
import math
pygame.init()
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

G = 2

class Planet:
    def __init__(self, x, y, mass, radius, color, hastighet_x=0, hastighet_y=0):
        self.x = x
        self.y = y
        self.mass = mass
        self.radius = radius
        self.color = color
        self.hastighet_x = hastighet_x
        self.hastighet_y = hastighet_y

    def apply_gravity(self, andraplaneter):
        dx = andraplaneter.x - self.x
        dy = andraplaneter.y - self.y
        längd = math.sqrt(dx**2 + dy**2)
        if längd == 0:
            return 0, 0
        force = G * self.mass * andraplaneter.mass / (längd ** 2)
        acc_x = force * dx / (self.mass * längd)
        acc_y = force * dy / (self.mass * längd)
        return acc_x, acc_y

    def trattaratta(self, acc_x, acc_y):
        self.hastighet_x += acc_x
        self.hastighet_y += acc_y
        self.x += self.hastighet_x
        self.y += self.hastighet_y

        if self.x - self.radius < 0 or self.x + self.radius > screen_width:
            self.hastighet_x *= -1
        if self.y - self.radius < 0 or self.y + self.radius > screen_height:
            self.hastighet_y *= -1

    def printmass(self):
        print("planetmass:"+str(self.mass))

planet1 = Planet(300, 300, 25, 50, RED, 0.5, 0)
planet2 = Planet(500, 300, 90, 30, BLUE, 0.6, 0)
planet3 = Planet(400, 100, 15, 40, GREEN, 0, 0.4)

planets = [planet1, planet2, planet3]

clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    screen.fill(WHITE)
    
    i = 0
    for planet in planets:
        print(planet.printmass())
        print("i:"+str(i))
        total_acc_x = 0
        total_acc_y = 0
        j = 0
        for other_planet in planets:
            print(other_planet.printmass())
            print("j:"+str(j))
            if i != j:
                acc_x, acc_y = planet.apply_gravity(other_planet)
                total_acc_x += acc_x
                total_acc_y += acc_y
            j += 1
        
        planet.trattaratta(total_acc_x, total_acc_y)
        
        pygame.draw.circle(screen, planet.color, (int(planet.x), int(planet.y)), planet.radius)
        i += 1
    
    pygame.display.flip()

    clock.tick(500)
