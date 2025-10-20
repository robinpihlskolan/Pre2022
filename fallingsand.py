import pygame
import random
import math
pygame.init()

width, height = 600, 400
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Sand Simulation")

w = 5 
cols = width // w
rows = height // w
hue_value = 200
grid = [[0 for _ in range(rows)] for _ in range(cols)]

def within_cols(i):
    return i>= 0 and i<=cols-1
def within_rows(j):
    return j >= 0 and j <= rows -1
def make_2d_array(cols, rows):
    return [[0 for _ in range(rows)] for _ in range(cols)]



def mouse(mouse_x, mouse_y):
    global hue_value
    global grid
    mouse_col = math.floor(mouse_x / w)
    mouse_row = math.floor(mouse_y / w)
    matrix = 5
    extent = math.floor(matrix / 2)
    for i in range(-extent, extent+1):
        for j in range(-extent, extent + 1):
            if random.random() < 0.75:
                col = mouse_col + i
                row = mouse_row + j
                if within_cols(col) and within_rows(row):
                    grid[col][row] = hue_value
                    
def draw_grid():
    global grid
 
    for i in range(cols):
        for j in range(rows):
            
            if grid[i][j] > 0:
                hue = grid[i][j]
                color = pygame.Color(255)
                color.hsva = (hue, 100, 100)  
                pygame.draw.rect(screen, color, (i * w, j * w, w, w))

def grid_update():
    global grid
    nextGrid = make_2d_array(cols, rows)
    for i in range(cols):
        for j in range(rows):
            state = grid[i][j]
            if state > 0:
                # Only proceed if j + 1 is within bounds
                if j + 1 < rows:
                    below = grid[i][j + 1]
                    dir = 1
                    if random.random() < 0.99:
                        dir *= -1

                    belowa = -1
                    belowb = -1

                    # Check within bounds for belowa and belowb
                    if within_cols(i + dir) and j + 1 < rows:
                        belowa = grid[i + dir][j + 1]
                    if within_cols(i - dir) and j + 1 < rows:
                        belowb = grid[i - dir][j + 1]

                    # Update nextGrid based on the state of cells below
                    if below == 0:
                        nextGrid[i][j + 1] = state
                    elif belowa == 0:
                        nextGrid[i + dir][j + 1] = state
                    elif belowb == 0:
                        nextGrid[i - dir][j + 1] = state
                    else:
                        nextGrid[i][j] = state
                else:
                    nextGrid[i][j] = state  # If at the bottom, keep the state in place

    grid = nextGrid
# Main program loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if pygame.mouse.get_pressed()[0]:  # Left mouse button
            mouse_x, mouse_y = pygame.mouse.get_pos()
            mouse(mouse_x, mouse_y)
    hue_value = (hue_value + 1) % 360 

    # Update and draw
    grid_update()
    screen.fill((0, 0, 0)) 
    draw_grid()
    pygame.display.flip()
    pygame.time.delay(30)

# Quit Pygame
pygame.quit()
