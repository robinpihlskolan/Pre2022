import pygame

# Initiera pygame
pygame.init()

# Fönsterinställningar
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Studsande Boll")

# Färger
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Bollens egenskaper
ball_radius = 20
ball_x = WIDTH // 2
ball_y = HEIGHT // 2
ball_speed_x = 4
ball_speed_y = 4

# Spel-loopen
running = True
clock = pygame.time.Clock()
while running:
    screen.fill(WHITE)  # Rensa skärmen
    
    # Händelsehantering
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Uppdatera bollens position
    ball_x += ball_speed_x
    ball_y += ball_speed_y
    
    # Studsa mot kanterna
    if ball_x - ball_radius <= 0 or ball_x + ball_radius >= WIDTH:
        ball_speed_x *= -1
    if ball_y - ball_radius <= 0 or ball_y + ball_radius >= HEIGHT:
        ball_speed_y *= -1
    
    # Rita bollen
    pygame.draw.circle(screen, RED, (ball_x, ball_y), ball_radius)
    
    # Uppdatera skärmen
    pygame.display.flip()
    clock.tick(60)  # Begränsa FPS

pygame.quit()
