import pygame
import sys
import random
import math

# Starta pygame
pygame.init()

# Inställningar
BREDD, HÖJD = 800, 600
PIXEL_STORLEK = 10  # Större pixlar för tydligare resultat

# Skapa fönster
skärm = pygame.display.set_mode((BREDD, HÖJD))
klocka = pygame.time.Clock()

# Variabler
mjuk_slump = False  # False = helt slumpmässig, True = mjuk slump
nytt_mönster = True

# funktion för mjuk slump
def get_mjuk_färg(x, y):
    """Skapa en färg baserad på position för mjuk övergång"""
    r = (math.sin(x * 0.05) + math.cos(y * 0.05)) * 127 + 128
    g = (math.sin(x * 0.03 + 1) + math.cos(y * 0.07)) * 127 + 128
    b = (math.sin(x * 0.06 + 2) + math.cos(y * 0.04 + 1)) * 127 + 128
    return ((int(r), int(g), int(b)))

# Huvudloop
körning = True
while körning:
    # Hantera händelser
    for händelse in pygame.event.get():
        if händelse.type == pygame.QUIT:
            körning = False
        elif händelse.type == pygame.KEYDOWN:
            if händelse.key == pygame.K_ESCAPE:
                körning = False
            elif händelse.key == pygame.K_SPACE:
                mjuk_slump = not mjuk_slump
                nytt_mönster = True
            elif händelse.key == pygame.K_r:
                nytt_mönster = True

    # Rita ny bild om det behövs
    if nytt_mönster:
        # Rita varje pixel
        for y in range(0, HÖJD, PIXEL_STORLEK):
            for x in range(0, BREDD, PIXEL_STORLEK):
                if mjuk_slump:
                    # Mjuk slump (baserad på position)
                    färg = get_mjuk_färg(x, y)
                else:
                    # Helt slumpmässig färg
                    färg = (random.randint(0, 255), 
                           random.randint(0, 255), 
                           random.randint(0, 255))
                
                # Rita pixeln
                pygame.draw.rect(skärm, färg, (x, y, PIXEL_STORLEK, PIXEL_STORLEK))
        
        nytt_mönster = False
    
    # Visa instruktioner
    font = pygame.font.SysFont(None, 30)
    text = "SPACE: Byt läge | R: Generera ny bild | ESC: Avsluta"
    text_yta = font.render(text, True, (255, 255, 255))
    skärm.blit(text_yta, (10, 10))
    
    läge = "Mjuk slump" if mjuk_slump else "Helt slumpmässig"
    text_läge = font.render(f"Läge: {läge}", True, (255, 255, 255))
    skärm.blit(text_läge, (10, 40))
    
    # Uppdatera skärmen
    pygame.display.flip()
    klocka.tick(30)

pygame.quit()
sys.exit()
