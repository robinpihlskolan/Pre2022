import numpy as np
import sounddevice as sd
import pygame
import random

# Pygame setup
WIDTH, HEIGHT = 400, 600
WHITE = (255, 255, 255)
BIRD_COLOR = (255, 255, 0)
PIPE_COLOR = (0, 255, 0)
GRAVITY = 0.5
FLAP_STRENGTH = -8
CLAP_THRESHOLD = 0.01  # Lowered threshold for better sensitivity
PIPE_SPEED = 3
PIPE_GAP = 150

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

class FlappyBirdGame:
    def __init__(self):
        self.bird_y = HEIGHT // 2
        self.bird_velocity = 0
        self.pipes = [(WIDTH, random.randint(100, HEIGHT - 200))]
        self.running = True
        self.buffer = np.zeros(44100 // 10)  # 0.1 sec buffer
        self.stream = sd.InputStream(callback=self.audio_callback, channels=1, samplerate=44100, blocksize=1024)
        self.stream.start()

    def audio_callback(self, indata, frames, time, status):
        if status:
            print(status)
        self.buffer = np.roll(self.buffer, -frames)
        self.buffer[-frames:] = indata[:, 0]

    def detect_clap(self):
        """Detects a clap based on sudden volume spikes."""
        rms_volume = np.sqrt(np.mean(self.buffer ** 2))  # Use RMS for better accuracy
        print(f"Detected Volume: {rms_volume:.4f}")  # Debugging
        return rms_volume > CLAP_THRESHOLD

    def update_bird(self):
        if self.detect_clap():
            self.bird_velocity = FLAP_STRENGTH
        self.bird_velocity += GRAVITY
        self.bird_y += self.bird_velocity

    def update_pipes(self):
        self.pipes = [(x - PIPE_SPEED, y) for x, y in self.pipes if x > -50]
        if self.pipes[-1][0] < WIDTH - 200:
            self.pipes.append((WIDTH, random.randint(100, HEIGHT - 200)))

    def check_collision(self):
        for x, y in self.pipes:
            if x < 60 < x + 50 and not (y < self.bird_y < y + PIPE_GAP):
                self.running = False
        if self.bird_y > HEIGHT or self.bird_y < 0:
            self.running = False

    def run(self):
        while self.running:
            screen.fill((0, 0, 0))
            self.update_bird()
            self.update_pipes()
            self.check_collision()

            # Draw bird
            pygame.draw.circle(screen, BIRD_COLOR, (60, int(self.bird_y)), 15)
            
            # Draw pipes
            for x, y in self.pipes:
                pygame.draw.rect(screen, PIPE_COLOR, (x, 0, 50, y))
                pygame.draw.rect(screen, PIPE_COLOR, (x, y + PIPE_GAP, 50, HEIGHT - y - PIPE_GAP))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            
            pygame.display.flip()
            clock.tick(30)

        self.stream.stop()
        self.stream.close()
        pygame.quit()

if __name__ == "__main__":
    game = FlappyBirdGame()
    game.run()
