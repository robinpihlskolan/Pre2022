import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fluid Simulation")

# Colors
BLACK = (0, 0, 0)
BLUE = (0, 100, 255)

# Particle properties
NUM_PARTICLES = 1000
PARTICLE_RADIUS = 4
GRAVITY = 0.2  # Always apply gravity
VISCOUS_FORCE = 0.98  # Friction to slow particles down gradually
INTERACTION_RADIUS = 20
REPULSION_FORCE = 0.1  # Weaker repulsion force to avoid bouncing too much
MAX_FORCE = 1.0
GROUND_FRICTION = 0.9  # Stronger friction to slow horizontal movement
BOUNCE_DAMPING = 0.7  # Gentle damping factor for bounce control
MIN_VELOCITY = 0.05  # Minimum threshold for considering particles as moving too slowly

# Grid properties for spatial partitioning
GRID_SIZE = 50  # Size of the grid cells for spatial partitioning
grid_width = WIDTH // GRID_SIZE
grid_height = HEIGHT // GRID_SIZE

# Initialize particles
particles = [
    {"pos": [random.uniform(100, 700), random.uniform(100, 400)],
     "vel": [random.uniform(-0.5, 0.5), random.uniform(-0.5, 0.5)]}
    for _ in range(NUM_PARTICLES)
]

# Helper function to clamp values
def clamp(value, min_val, max_val):
    return max(min_val, min(value, max_val))

# Helper function to get the grid cell for a particle
def get_grid_cell(particle):
    return (int(particle["pos"][0] // GRID_SIZE), int(particle["pos"][1] // GRID_SIZE))

# Simulation loop
clock = pygame.time.Clock()
running = True

# List to hold the particles in each grid cell
grid = {}

while running:
    screen.fill(BLACK)

    # Update grid
    for cell in grid.values():
        cell.clear()

    # Fill the grid with particles
    for particle in particles:
        cell = get_grid_cell(particle)
        if cell not in grid:
            grid[cell] = []
        grid[cell].append(particle)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update particles
    for particle in particles:
        # Apply gravity continuously
        particle["vel"][1] += GRAVITY  # Gravity pulls downward

        # Track interaction force accumulations
        total_repulsion = [0, 0]

        # Get the grid cell of the particle
        cell = get_grid_cell(particle)

        # Check neighboring grid cells (including the current one)
        neighbors = []
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                neighbor_cell = (cell[0] + dx, cell[1] + dy)
                if neighbor_cell in grid:
                    neighbors.extend(grid[neighbor_cell])

        # Check interactions with nearby particles
        for other in neighbors:
            if particle == other:
                continue

            # Calculate distance between particles
            dx = other["pos"][0] - particle["pos"][0]
            dy = other["pos"][1] - particle["pos"][1]
            dist = math.sqrt(dx**2 + dy**2)

            if 0 < dist < INTERACTION_RADIUS:
                # Repulsion force: Prevents overlapping
                repulsion = clamp(REPULSION_FORCE / (dist + 0.1), 0, MAX_FORCE)
                total_repulsion[0] -= repulsion * (dx / dist)
                total_repulsion[1] -= repulsion * (dy / dist)

        # Apply interaction forces
        particle["vel"][0] += total_repulsion[0]
        particle["vel"][1] += total_repulsion[1]

        # Update position
        particle["pos"][0] += particle["vel"][0]
        particle["pos"][1] += particle["vel"][1]

        # Apply viscous damping to slow down the movement gradually
        particle["vel"][0] *= VISCOUS_FORCE
        particle["vel"][1] *= VISCOUS_FORCE

        # Handle ground collisions with vertical damping (stop bouncing too much)
        if particle["pos"][1] >= HEIGHT - PARTICLE_RADIUS:
            particle["pos"][1] = HEIGHT - PARTICLE_RADIUS  # Prevent particles from sinking below the floor

            # Apply bounce with a moderate bounce factor
            if particle["vel"][1] > 0:  # Only apply bounce if falling
                particle["vel"][1] *= -BOUNCE_DAMPING  # Bounce but with some energy loss

            # Apply stronger horizontal friction to stop horizontal movement
            particle["vel"][0] *= GROUND_FRICTION

            # Vertical damping for particles close to the ground
            if abs(particle["vel"][1]) < MIN_VELOCITY:
                particle["vel"][1] = 0  # Stop vertical movement if too small

        # Handle side collisions (reduce energy to prevent "climbing" sides)
        if particle["pos"][0] <= PARTICLE_RADIUS or particle["pos"][0] >= WIDTH - PARTICLE_RADIUS:
            particle["vel"][0] *= -0.5  # Reflect velocity with energy loss

        # Prevent particles from leaving screen bounds horizontally
        particle["pos"][0] = max(PARTICLE_RADIUS, min(WIDTH - PARTICLE_RADIUS, particle["pos"][0]))

        # If the particle's velocity is below a threshold, stop it from moving
        if abs(particle["vel"][0]) < MIN_VELOCITY and abs(particle["vel"][1]) < MIN_VELOCITY:
            # Essentially stop the particle if it is no longer moving
            particle["vel"] = [0, 0]

    # Draw particles
    for particle in particles:
        pygame.draw.circle(screen, BLUE, (int(particle["pos"][0]), int(particle["pos"][1])), PARTICLE_RADIUS)

    # Display updated frame
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
