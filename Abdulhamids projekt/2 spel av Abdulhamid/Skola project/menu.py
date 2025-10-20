import pygame
import sys
from settings import *
import os

class Menu:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()  
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("IDK Menu")
        
        self.background = pygame.image.load("./bk.png")


        try:
            pygame.mixer.music.load("./sounds/menu_sound.mp3")
            pygame.mixer.music.set_volume(0.5)  
            pygame.mixer.music.play(-1)  
        except OSError as err:
            print("OS error:", err)
        
        self.font = pygame.font.Font(None, 36)

    def draw_button(self, text, y_position, is_selected=False):
        text_surface = self.font.render(text, True, BLACK)
        text_rect = text_surface.get_rect(center=(WIDTH//2, y_position))
        
        button_rect = pygame.Rect(text_rect.x - 20, text_rect.y - 10, 
                                  text_rect.width + 40, text_rect.height + 20)
        
        pygame.draw.rect(self.screen, 
                         (200,200,200) if is_selected else (255, 255, 255), 
                         button_rect)
        pygame.draw.rect(self.screen, BLACK, button_rect, 2)
        
        self.screen.blit(text_surface, text_rect)
        return button_rect

    def run(self):
        selected_option = 0
        
        while True:
            self.screen.blit(self.background, (0, 0))  # Draw background image
            
            play_button = self.draw_button("Play", 200, selected_option == 0)
            quit_button = self.draw_button("Quit", 300, selected_option == 1)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.mixer.music.stop()
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        selected_option = (selected_option - 1) % 2
                    elif event.key == pygame.K_DOWN:
                        selected_option = (selected_option + 1) % 2
                    
                    if event.key == pygame.K_RETURN:
                        if selected_option == 0:  # Play
                            pygame.mixer.music.stop()
                            return True
                        elif selected_option == 1:  # Quit
                            pygame.mixer.music.stop()
                            pygame.quit()
                            sys.exit()

            pygame.display.flip()

if __name__ == "__main__":
    menu = Menu()
    menu.run()
