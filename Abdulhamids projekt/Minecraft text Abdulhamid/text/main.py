import pygame
from text_effect import TextEffect
from input_field import InputField

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 1200, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Create instances
effect = TextEffect(WIDTH, HEIGHT)
input_field = InputField(20, 20, 400, 40)

# Initialize with default text
effect.update_text(effect.text)

# Main loop
running = True
clock = pygame.time.Clock()

while running:
    mouse_x, mouse_y = pygame.mouse.get_pos()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # Handle input field
        if input_field.handle_event(event):
            effect.update_text(input_field.text)
    
    # Clear screen
    screen.fill((0, 0, 0))
    
    # Draw particles
    effect.render(screen, mouse_x, mouse_y)
    
    # Draw input field
    input_field.draw(screen)
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()