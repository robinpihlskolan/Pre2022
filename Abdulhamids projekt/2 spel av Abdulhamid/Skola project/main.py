import pygame
import random
from settings import *
from menu import Menu
from sound import GameSounds
from Player import Player
from Platform import Platform
from PowerUp import PowerUp

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("IDK")
game_sounds = GameSounds()


player = Player()
platforms = [Platform(WIDTH//2, HEIGHT-50)]
power_ups = []
score = 0
last_platform = None  

PLATFORM_TYPES = {
    "normal": 0.6,    
    "moving": 0.2,   
    "breaking": 0.15,
    "spring": 0.05    
}



menu = Menu()
menu.run()


def get_random_platform_type():
    rand = random.random()
    cumulative = 0
    for ptype, prob in PLATFORM_TYPES.items():
        cumulative += prob
        if rand <= cumulative:
            return ptype
    return "normal"

for i in range(10):
    x = random.randint(0, WIDTH-Platform_WIDTH)
    y = i * 60
    platform_type = get_random_platform_type()
    platform = Platform(x, y, platform_type)
    platforms.append(platform)

running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and player.has_jetpack and player.jetpack_fuel > 0:
                player.hastighet_y = -12
                player.jetpack_fuel -= 0.25

    if player.has_jetpack and player.jetpack_fuel <= 0:
        player.has_jetpack = False  
        print("Jetpack depleted!")

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player.x > 0:
        player.x -= player.speed
    if keys[pygame.K_RIGHT] and player.x < WIDTH - player.width:
        player.x += player.speed
    
    if keys[pygame.K_SPACE] and player.has_jetpack and player.jetpack_fuel > 0:
        player.hastighet_y = max(player.hastighet_y - 1, -12)
        player.jetpack_fuel -= 0.25
    else:
        player.hastighet_y += GRAVITY
    player.y += player.hastighet_y

    if player.spring_boost:
        player.spring_timer -= 1
        if player.spring_timer <= 0:
            player.spring_boost = False
            player.jump_speed = Player_Jump_Speed


    player_rect = pygame.Rect(player.x, player.y, player.width, player.height)
    for platform in platforms[:]:
        platform.update()
        if player_rect.colliderect(platform.rect) and player.hastighet_y > 0:
            if platform != last_platform:
                if platform.type == "breaking":
                    platforms.remove(platform)
                    score += 15
                elif platform.type == "spring":
                    player.spring_boost = True
                    player.spring_timer = 20
                    player.hastighet_y = -25
                    score += 25
                elif platform.type == "moving":
                    player.hastighet_y = player.jump_speed
                    score += 10
                else:
                    player.hastighet_y = player.jump_speed
                    score += 5
                
                last_platform = platform  
            else:
                player.hastighet_y = player.jump_speed
            
            if random.random() < 0.08:
                power_ups.append(PowerUp(
                    random.randint(0, WIDTH - Powerup_WIDTH),
                    platform.y - 150
                ))
            
            if platform.type == "spring":
               game_sounds.play_spring_jump()
            elif platform.type == "normal" or platform.type == "moving":
                game_sounds.play_normal_jump()
            if platform.type == "breaking":
                game_sounds.play_red_platform()
        

    for power_up in power_ups[:]:
        if player_rect.colliderect(power_up.rect):
            if power_up.type == "jetpack":
                player.has_jetpack = True
                player.jetpack_fuel = 100
                score += 50
            power_ups.remove(power_up)
    
    if player.y < HEIGHT // 2:
        offset = HEIGHT // 2 - player.y
        player.y += offset
        
        for platform in platforms:
            platform.y += offset
            platform.rect.y = platform.y
        for power_up in power_ups:
            power_up.y += offset
            power_up.rect.y = power_up.y
        
        platforms = [p for p in platforms if p.y < HEIGHT]
        power_ups = [p for p in power_ups if p.y < HEIGHT]
        
        if last_platform not in platforms:
            last_platform = None
        
        while len(platforms) < 10:
            x = random.randint(0, WIDTH - Platform_WIDTH)
            y = min([p.y for p in platforms]) - 60
            platform_type = get_random_platform_type()
            platforms.append(Platform(x, y, platform_type))

    if player.y > HEIGHT:
        print(f"Game Over! Final Score: {score}")
        running = False    
    
    player.update_animation()
    screen.fill(WHITE)
    
    for platform in platforms:
        platform.draw(screen)
    
    for power_up in power_ups:
        power_up.draw(screen)
    
    player.draw(screen)
    
    font = pygame.font.Font(None, 36)
    score_text = font.render(f'Score: {score}', True, (0, 0, 0))
    screen.blit(score_text, (10, 10))
    
    if player.has_jetpack:
        fuel_percent = int((player.jetpack_fuel / 100) * 100)
        fuel_text = font.render(f'Jetpack: {fuel_percent}', True, (0, 0, 0))
        screen.blit(fuel_text, (10, 40))
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()