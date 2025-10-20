import pygame
import random
import math
from settings import *

class Particle:
    def __init__(self, x, y, color, lifetime=45):
        self.x = x
        self.y = y
        self.color = color
        self.lifetime = lifetime
        self.max_lifetime = lifetime
        self.dx = random.uniform(-1, 1)
        self.dy = random.uniform(0, 2)
        self.size = random.uniform(1, 2)  # reduced particle size
        self.alpha = 255

    def update(self):
        self.x += self.dx
        self.y += self.dy
        self.lifetime -= 1
        self.alpha = int(255 * (self.lifetime / self.max_lifetime) ** 1.5)
        # Keep size more consistent, just slight reduction
        self.size = max(0.5, self.size * (self.lifetime / self.max_lifetime))

    def draw(self, screen):
        surf = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
        pygame.draw.circle(surf, (*self.color, self.alpha), 
                         (self.size, self.size), self.size)
        screen.blit(surf, (self.x - self.size, self.y - self.size))

class Trail:
    def __init__(self, max_points=10):
        self.points = []
        self.max_points = max_points

    def update(self, x, y):
        self.points.append((x, y))
        if len(self.points) > self.max_points:
            self.points.pop(0)

    def draw(self, screen):
        if len(self.points) < 2:
            return
        
        for i in range(len(self.points) - 1):
            alpha = int(255 * (i / len(self.points)))
            pygame.draw.line(screen, (*BLUE, alpha), 
                           self.points[i], self.points[i + 1], 2)

class Player:
    def __init__(self):
        self.width = Player_WIDTH
        self.height = Player_HEIGHT
        self.x = WIDTH // 2
        self.y = HEIGHT - 100
        self.speed = Player_Speed
        self.jump_speed = Player_Jump_Speed
        self.hastighet_y = 0
        self.has_jetpack = False
        self.jetpack_fuel = 0
        self.spring_boost = False
        self.spring_timer = 0
        
        # Animation properties
        self.particles = []
        self.trail = Trail()
        self.eye_blink = 0
        self.mouth_expression = 0
        
    def update_animation(self):
        self.trail.update(self.x + self.width/2, self.y + self.height/2)
        
        # Update existing particles
        self.particles = [p for p in self.particles if p.lifetime > 0]
        for particle in self.particles:
            particle.update()
            
        # Create particles when moving
        if self.hastighet_y < 0:  # If jumping
            for _ in range(5):  # Increased number of particles since they're smaller
                particle = Particle(
                    self.x + random.randint(0, self.width),
                    self.y + self.height + random.randint(-1, 1),
                    (180, 180, 255)
                )
                self.particles.append(particle)
                
        # eye blinking
        if random.random() < 0.01:
            self.eye_blink = 5
        elif self.eye_blink > 0:
            self.eye_blink -= 1
            
    
    def draw(self, screen):
        # Draw particles first (so they appear behind the player)
        for particle in self.particles:
            particle.draw(screen)
            
        # Draw trail
        self.trail.draw(screen)
        
        # Draw player body
        pygame.draw.rect(screen, BLUE, (self.x, self.y, self.width, self.height))
        
        # Draw face
        eye_height = 15 if self.eye_blink == 0 else 13
        pygame.draw.circle(screen, WHITE, (self.x + 10, self.y + eye_height), 5)
        pygame.draw.circle(screen, WHITE, (self.x + 30, self.y + eye_height), 5)
        pygame.draw.circle(screen, (0, 0, 0), (self.x + 10, self.y + eye_height), 2)
        pygame.draw.circle(screen, (0, 0, 0), (self.x + 30, self.y + eye_height), 2)
        
        # Draw jetpack (if equipped)
        if self.has_jetpack:
            pygame.draw.rect(screen, RED, (self.x-10, self.y+10, 10, 20))
            flame_offset = random.randint(-5, 5)
            pygame.draw.polygon(screen, YELLOW, [
                (self.x-15, self.y+35),
                (self.x-5, self.y+35),
                (self.x-10, self.y+45+flame_offset)
            ])