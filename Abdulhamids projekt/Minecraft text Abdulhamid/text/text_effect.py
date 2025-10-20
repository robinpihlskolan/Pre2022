import pygame
from particle import Particle

class TextEffect:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.max_text_width = self.width * 0.8
        self.font_size = 100
        self.text_vertical_offset = 0
        self.line_height = self.font_size * 1.2
        self.text_x = self.width / 2
        self.text_y = self.height / 2 - self.line_height / 2
        self.particles = []
        self.gap = 3
        self.mouse_radius = 20000
        self.text = "TEXT PARTICLES"
        
        # Colors
        self.WHITE = (255, 255, 255)
        self.RED = (255, 0, 0)
        self.PURPLE = (128, 0, 128)
        self.FUCHSIA = (255, 0, 255)
        
        # Font setup
        self.font = pygame.font.Font("./minecraft_font.ttf", 100)

        
    def create_gradient_text(self, text):
        # This function simulates the linear gradient effect        
        words = text.split(' ')
        lines = []
        line = ''
        line_counter = 0
        
        for word in words:
            test_line = line + word + ' '
            text_surface = self.font.render(test_line, True, self.WHITE)
            if text_surface.get_width() > self.max_text_width:
                lines.append(line)
                line = word + ' '
                line_counter += 1
            else:
                line = test_line
        
        lines.append(line)  
        
        text_height = self.line_height * line_counter
        self.text_y = self.height/2 - text_height/2 + self.text_vertical_offset
        
        text_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        
        # Render each line
        for i, line in enumerate(lines):
            text1 = self.font.render(line, True, self.RED)
            text2 = self.font.render(line, True, self.FUCHSIA)
            text3 = self.font.render(line, True, self.PURPLE)
            
            # Calculate positions for blending
            pos_y = self.text_y + (i * self.line_height)
            text_width = text1.get_width()
            
            text_surface.blit(text1, (self.text_x - text_width/2, pos_y))
            text_surface.blit(text2, (self.text_x - text_width/2 + 2, pos_y), special_flags=pygame.BLEND_RGB_ADD)
            text_surface.blit(text3, (self.text_x - text_width/2 + 4, pos_y), special_flags=pygame.BLEND_RGB_ADD)
            
            for dx, dy in [(-2,0), (2,0), (0,-2), (0,2)]:
                outline = self.font.render(line, True, self.WHITE)
                text_surface.blit(outline, (self.text_x - text_width/2 + dx, pos_y + dy))
        
        return text_surface

    def convert_to_particles(self, text_surface):
        self.particles = []
        
        # Get pixel data from the text surface
        for y in range(0, self.height, self.gap):
            for x in range(0, self.width, self.gap):
                if x < text_surface.get_width() and y < text_surface.get_height():
                    color = text_surface.get_at((x, y))
                    
                    # Only create particles for visible pixels (non-transparent)
                    if color[3] > 0:  
                        self.particles.append(Particle(self, x, y, color))

    def update_text(self, new_text):
        self.text = new_text
        text_surface = self.create_gradient_text(self.text)
        self.convert_to_particles(text_surface)

    def render(self, surface, mouse_x, mouse_y):
        for particle in self.particles:
            particle.update(mouse_x, mouse_y)
            particle.draw(surface)
