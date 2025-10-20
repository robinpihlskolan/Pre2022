import pygame
import sys
import random


pygame.init()

# Screen Setup
WIDTH, HEIGHT = 800, 800
GRID_SIZE = 50
FONT =pygame.font.Font("./font.ttf",100)
MENU_FONT = pygame.font.Font("./font.ttf", 50)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Colors
GRID_COLOR = (40, 40, 40)
SNAKE_COLOR = (0, 200, 0)
APPLE_COLOR = (255, 50, 50)
SNAKE_OUTLINE = (0, 255, 0)
BACKGROUND_COLOR = (15, 15, 15)
TEXT_COLOR = (255, 255, 255)

eat_sound = pygame.mixer.Sound("./sound/eat.mp3")
death_sound = pygame.mixer.Sound("./sound/gameover.mp3")



class Snake:
    def __init__(self):
        self.x, self.y = GRID_SIZE, GRID_SIZE
        self.xdir = 1
        self.ydir = 0
        self.head = pygame.Rect(self.x, self.y, GRID_SIZE, GRID_SIZE)
        self.body = [pygame.Rect(self.x - GRID_SIZE, self.y, GRID_SIZE, GRID_SIZE)]
        self.dead = False

    def update(self):
        global apple

        for part in self.body:
            if self.head.colliderect(part):
                self.dead = True


        if not (0 <= self.head.x < WIDTH and 0 <= self.head.y < HEIGHT):
            self.dead = True

        if self.dead:
            death_sound.play()
            for _ in range(5):  
                screen.fill((255, 50, 50))
                pygame.display.update()
                pygame.time.delay(50)
                screen.fill(BACKGROUND_COLOR)
                pygame.display.update()
                pygame.time.delay(50)

            self.__init__()  
            apple = Apple() 

        self.body.append(self.head.copy())
        self.head.x += self.xdir * GRID_SIZE
        self.head.y += self.ydir * GRID_SIZE
        self.body.pop(0)

    def draw(self):
        for part in self.body:
            pygame.draw.rect(screen, SNAKE_COLOR, part)
            pygame.draw.rect(screen, SNAKE_OUTLINE, part, 3)  
        pygame.draw.rect(screen, (0, 255, 0), self.head)
        pygame.draw.rect(screen, (255, 255, 255), self.head, 3)  

class Apple:
    def __init__(self):
        self.x = random.randint(0, (WIDTH - GRID_SIZE) // GRID_SIZE) * GRID_SIZE
        self.y = random.randint(0, (HEIGHT - GRID_SIZE) // GRID_SIZE) * GRID_SIZE
        self.rect = pygame.Rect(self.x, self.y, GRID_SIZE, GRID_SIZE)

    def draw(self):
        pygame.draw.rect(screen, APPLE_COLOR, self.rect)
        pygame.draw.rect(screen, (255, 200, 200), self.rect.inflate(-10, -10))  


def draw_grid():
    for x in range(0, WIDTH, GRID_SIZE):
        for y in range(0, HEIGHT, GRID_SIZE):
            pygame.draw.rect(screen, GRID_COLOR, (x, y, GRID_SIZE, GRID_SIZE), 1)

def main_menu():
    while True:

        screen.fill(BACKGROUND_COLOR)
        title = FONT.render("Snake Game", True, TEXT_COLOR)
        start_text = MENU_FONT.render("Press ENTER to Start", True, TEXT_COLOR)
        quit_text = MENU_FONT.render("Press ESC to Quit", True, TEXT_COLOR)
        screen.blit(title, (WIDTH // 2 - 200, HEIGHT // 3))
        screen.blit(start_text, (WIDTH // 2 - 150, HEIGHT // 2))
        screen.blit(quit_text, (WIDTH // 2 - 150, HEIGHT // 2 + 50))
        pygame.display.update()
        
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

main_menu()
snake = Snake()
apple = Apple()

while True:
    screen.fill(BACKGROUND_COLOR)
    draw_grid()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN and snake.ydir == 0:
                snake.ydir, snake.xdir = 1, 0
            elif event.key == pygame.K_UP and snake.ydir == 0:
                snake.ydir, snake.xdir = -1, 0
            elif event.key == pygame.K_RIGHT and snake.xdir == 0:
                snake.ydir, snake.xdir = 0, 1
            elif event.key == pygame.K_LEFT and snake.xdir == 0:
                snake.ydir, snake.xdir = 0, -1

    snake.update()
    apple.draw()
    snake.draw()

    
    if snake.head.colliderect(apple.rect):
        eat_sound.play()
        snake.body.append(snake.body[-1].copy())  
        apple = Apple()  

    score_text = FONT.render(f"{len(snake.body) + 1}", True, "white")
    screen.blit(score_text, (WIDTH // 2 - 20, 20))

    pygame.display.update()
    clock.tick(10)  
