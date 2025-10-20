import pygame

class InputField:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = (100, 100, 100)
        self.text = "TEXT PARTICLES"
        self.active = False
        self.font = pygame.font.Font("./minecraft_font.ttf", 24)
        self.WHITE = (255, 255, 255)
        
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = True
            else:
                self.active = False
                
        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN:
                self.active = False
                return True
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                self.text += event.unicode
        return False
    
    def draw(self, surface):
        pygame.draw.rect(surface, (50, 50, 50) if self.active else self.color, self.rect)
        pygame.draw.rect(surface, self.WHITE, self.rect, 2)
        
        text_surface = self.font.render(self.text, True, self.WHITE)
        surface.blit(text_surface, (self.rect.x + 5, self.rect.y + 5))
