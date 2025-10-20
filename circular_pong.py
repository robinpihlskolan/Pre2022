import pygame
import sys
import math
import random # Importera random för slumpmässiga riktningar

# --- Spelinställningar ---
WIDTH, HEIGHT = 800, 600
FPS = 60
CENTER_X, CENTER_Y = WIDTH // 2, HEIGHT // 2
CIRCLE_RADIUS = 200  # Radien för paddelns cirkulära bana
PADDLE_WIDTH = 80    # Bredd på paddeln
PADDLE_HEIGHT = 15   # Höjd på paddeln
PADDLE_SPEED = 0.05  # Hur snabbt paddeln rör sig runt cirkeln (radianer per frame)
BALL_RADIUS = 15
BALL_BASE_SPEED = 3.0  # Bashastighet för bollen
MAX_BOUNCE_DEVIATION_ANGLE = math.pi / 4 # Max vinkelavvikelse från den inåtriktade normalen (45 grader)
SCORE = 0

# Färger
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

class Paddle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Skapa paddelns ursprungliga yta och spara den.
        # Denna yta kommer alltid att vara oförändrad för att undvika distorsion vid rotation.
        self.original_image = pygame.Surface([PADDLE_WIDTH, PADDLE_HEIGHT], pygame.SRCALPHA)
        self.original_image.fill(BLUE)
        
        # Den aktuella bilden som ritas (roteras från originalet)
        self.image = self.original_image 
        self.rect = self.image.get_rect()
        self.angle = 0  # Aktuell vinkel i radianer (position på cirkeln)
        # Den faktiska rotationsvinkeln för paddelns bild i radianer
        self.rotation_angle_radians = 0 

    def update(self, keys):
        # Uppdatera vinkeln baserat på tangenttryckningar
        if keys[pygame.K_LEFT]:
            self.angle -= PADDLE_SPEED
        if keys[pygame.K_RIGHT]:
            self.angle += PADDLE_SPEED

        # Beräkna paddelns position på cirkeln med trigonometri
        self.rect.centerx = CENTER_X + int(CIRCLE_RADIUS * math.cos(self.angle))
        self.rect.centery = CENTER_Y + int(CIRCLE_RADIUS * math.sin(self.angle))

        # Beräkna den faktiska rotationsvinkeln i radianer för paddelns bild.
        # Paddeln är tangentiell, så dess långa axel är vinkelrät mot den radiella vektorn.
        # Om den radiella vektorn är vid 'self.angle', är den tangentiella vinkeln 'self.angle + pi/2'.
        self.rotation_angle_radians = self.angle + math.pi / 2 
        
        # Pygame's rotate-funktion roterar moturs för positiva vinklar.
        # Vi behöver rotera med den negativa vinkeln för att matcha vår matematiska vinkel.
        rotation_angle_degrees = math.degrees(-self.rotation_angle_radians)
        
        self.image = pygame.transform.rotate(self.original_image, rotation_angle_degrees)
        # Uppdatera rektangeln efter rotation för att bibehålla korrekt centrum
        self.rect = self.image.get_rect(center=(self.rect.centerx, self.rect.centery))

    # Hjälpfunktion för att få paddelns normalvektor (pekar utåt från dess "fram"-yta)
    # Denna används för studslogiken, inte för penetrationslösning.
    def get_normal_vector(self):
        # Paddelns "fram"-yta är den som vetter mot cirkelns centrum.
        # Normalvektorn som pekar *ut* från denna yta är den radiella vektorn
        # från cirkelns centrum till paddelns position.
        return (math.cos(self.angle), math.sin(self.angle))


class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Skapa bollens yta och rita en cirkel på den
        self.image = pygame.Surface([BALL_RADIUS * 2, BALL_RADIUS * 2], pygame.SRCALPHA) # SRCALPHA för transparens
        pygame.draw.circle(self.image, RED, (BALL_RADIUS, BALL_RADIUS), BALL_RADIUS)
        self.rect = self.image.get_rect()
        self.rect.center = (CENTER_X, CENTER_Y)  # Starta bollen i mitten av skärmen
        self.velocity = [0, 0] # Initial hastighet, sätts slumpmässigt i reset_ball
        self.reset_ball() # Kalla på reset_ball för att sätta initial position och hastighet

    def update(self):
        # Uppdatera bollens position baserat på dess hastighet
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]

        # Studsa från skärmkanterna för att hålla bollen inom fönstret
        if self.rect.left < 0 or self.rect.right > WIDTH:
            self.velocity[0] *= -1 # Vänd x-riktningen
        if self.rect.top < 0 or self.rect.bottom > HEIGHT:
            self.velocity[1] *= -1 # Vänd y-riktningen

    def reset_ball(self):
        # Återställ bollen till mitten
        self.rect.center = (CENTER_X, CENTER_Y)
        
        # Ge bollen en slumpmässig riktning vid start
        random_angle = random.uniform(0, 2 * math.pi) # Slumpmässig vinkel i radianer
        self.velocity = [BALL_BASE_SPEED * math.cos(random_angle), BALL_BASE_SPEED * math.sin(random_angle)]

def main():
    global SCORE # Gör SCORE tillgänglig globalt för att kunna ändra den

    pygame.init() # Initiera Pygame
    screen = pygame.display.set_mode((WIDTH, HEIGHT)) # Skapa spel-fönstret
    pygame.display.set_caption("Cirkel-Pong") # Sätt fönstertitel
    clock = pygame.time.Clock() # Skapa en klocka för att kontrollera FPS
    font = pygame.font.Font(None, 74) # Skapa ett typsnitt för att visa poäng och meddelanden

    # Skapa sprite-grupper för att hantera spelobjekt
    all_sprites = pygame.sprite.Group()
    paddle = Paddle() # Skapa paddel-objektet
    ball = Ball()     # Skapa boll-objektet
    all_sprites.add(paddle, ball) # Lägg till paddel och boll i sprite-gruppen

    running = True    # Huvudloop-flagga
    game_over = False # Spel över-flagga

    # Huvudspelloop
    while running:
        # Hantera händelser (t.ex. stänga fönstret, tangenttryckningar)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False # Avsluta loopen om fönstret stängs
            if event.type == pygame.KEYDOWN: # Kontrollera KEYDOWN-händelser här
                if game_over and event.key == pygame.K_r:
                    # Återställ spelet om det är över och 'R' trycks
                    SCORE = 0
                    ball.reset_ball()
                    game_over = False
                if game_over and event.key == pygame.K_q:
                    running = False # Avsluta spelet om 'Q' trycks när det är över

        # Uppdatera spelobjekt om spelet inte är över
        if not game_over:
            keys = pygame.key.get_pressed() # Hämta alla nedtryckta tangenter
            paddle.update(keys) # Uppdatera paddelns position
            ball.update()       # Uppdatera bollens position

            # --- Manuell kollisionsdetektion mellan boll och paddel (Cirkel-Roterad Rektangel) ---
            # 1. Hämta bollens och paddelns centrumkoordinater
            ball_center_x, ball_center_y = ball.rect.center
            paddle_center_x, paddle_center_y = paddle.rect.center

            # 2. Beräkna vektorn från paddelns centrum till bollens centrum
            vec_x = ball_center_x - paddle_center_x
            vec_y = ball_center_y - paddle_center_y

            # 3. Rotera denna vektor till paddelns lokala koordinatsystem
            # För att få bollens position i paddelns lokala system, rotera med den negativa av paddelns rotationsvinkel.
            cos_neg_rot = math.cos(-paddle.rotation_angle_radians)
            sin_neg_rot = math.sin(-paddle.rotation_angle_radians)

            local_ball_x = vec_x * cos_neg_rot - vec_y * sin_neg_rot
            local_ball_y = vec_x * sin_neg_rot + vec_y * cos_neg_rot

            # 4. Hitta närmaste punkt på den axel-justerade paddeln till den lokala bollens centrum
            half_pw = PADDLE_WIDTH / 2
            half_ph = PADDLE_HEIGHT / 2

            closest_x = max(-half_pw, min(local_ball_x, half_pw))
            closest_y = max(-half_ph, min(local_ball_y, half_ph))

            # 5. Beräkna avståndet från den lokala bollens centrum till närmaste punkt
            dist_x = local_ball_x - closest_x
            dist_y = local_ball_y - closest_y
            distance_squared = dist_x**2 + dist_y**2

            # 6. Kollision om avståndet är mindre än bollens radie
            if distance_squared <= BALL_RADIUS**2:
                SCORE += 1
                
                # --- Kollisionsrespons: Lös penetration först ---
                # Beräkna överlappningens djup
                overlap = BALL_RADIUS - math.sqrt(distance_squared)
                
                # Beräkna den exakta normalvektorn för penetrationen
                # Detta är vektorn från närmaste punkt på paddeln till bollens centrum, roterad tillbaka till världskoordinater.
                cos_rot = math.cos(paddle.rotation_angle_radians)
                sin_rot = math.sin(paddle.rotation_angle_radians)
                
                # Rotera dist_x, dist_y (som är i paddelns lokala system) tillbaka till världskoordinater
                penetration_normal_x = dist_x * cos_rot - dist_y * sin_rot
                penetration_normal_y = dist_x * sin_rot + dist_y * cos_rot

                # Normalisera penetrationsnormalen
                normal_magnitude = math.hypot(penetration_normal_x, penetration_normal_y)
                if normal_magnitude == 0: # Undvik division med noll om bollen är exakt i mitten av paddeln
                    # Fallback: Använd paddelns radiella normal om ingen specifik penetrationsnormal kan beräknas
                    penetration_normal_x, penetration_normal_y = paddle.get_normal_vector()
                else:
                    penetration_normal_x /= normal_magnitude
                    penetration_normal_y /= normal_magnitude

                # Flytta bollen ut från paddeln längs den beräknade penetrationsnormalen
                ball.rect.x += penetration_normal_x * overlap
                ball.rect.y += penetration_normal_y * overlap

                # --- Studslogik: Rikta bollen inåt med avvikelse ---
                # hit_offset_ratio är ett värde mellan -1 (vänster kant) och 1 (höger kant)
                # i paddelns lokala koordinatsystem.
                hit_offset_ratio = local_ball_x / half_pw 

                # Den "inåtriktade" normalen är paddelns vinkel + PI (180 grader)
                # Detta pekar direkt mot cirkelns centrum
                inward_normal_angle = paddle.angle + math.pi
                
                # Beräkna den nya utgående vinkeln baserat på den inåtriktade normalen
                # och avvikelsen från träffpunkten.
                # En positiv hit_offset_ratio (höger träff) ska ge en vinkel som är mer "moturs" (större vinkel).
                # En negativ hit_offset_ratio (vänster träff) ska ge en vinkel som är mer "medurs" (mindre vinkel).
                new_outgoing_angle = inward_normal_angle + (hit_offset_ratio * MAX_BOUNCE_DEVIATION_ANGLE)

                # Sätt bollens nya hastighet baserat på den beräknade vinkeln och bashastigheten
                ball.velocity[0] = BALL_BASE_SPEED * math.cos(new_outgoing_angle)
                ball.velocity[1] = BALL_BASE_SPEED * math.sin(new_outgoing_angle)
                
            # Kontrollera om bollen lämnar den cirkulära banan
            # Beräkna avståndet från bollens centrum till cirkelns centrum
            distance_from_center = math.hypot(ball.rect.centerx - CENTER_X, ball.rect.centery - CENTER_Y)
            # Om bollen är för långt bort från cirkelns centrum, är spelet över
            if distance_from_center > CIRCLE_RADIUS + BALL_RADIUS + 20: # Liten marginal för att undvika omedelbar Game Over
                game_over = True

        # --- Rita allt på skärmen ---
        screen.fill(BLACK) # Fyll bakgrunden med svart

        # Rita den cirkulära banan för paddeln (valfritt, för visuell hjälp)
        pygame.draw.circle(screen, WHITE, (CENTER_X, CENTER_Y), CIRCLE_RADIUS, 1) # Rita en tunn vit cirkel

        all_sprites.draw(screen) # Rita alla sprites (paddel och boll)

        # Visa poäng på skärmen
        score_text = font.render(f"Poäng: {SCORE}", True, WHITE) # Skapa textytan
        screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 20)) # Rita texten centrerad högst upp

        # Visa "Game Over" meddelande om spelet är slut
        if game_over:
            game_over_text = font.render("Game Over!", True, WHITE)
            restart_text = font.render("Tryck 'R' för att spela igen eller 'Q' för att avsluta", True, WHITE)
            screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 50))
            screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 10))


        pygame.display.flip() # Uppdatera hela skärmen för att visa det som ritats
        clock.tick(FPS)      # Begränsa spelets hastighet till den angivna FPS

    pygame.quit() # Avsluta Pygame
    sys.exit()    # Avsluta programmet

if __name__ == "__main__":
    main() # Kör huvudfunktionen när skriptet startas
