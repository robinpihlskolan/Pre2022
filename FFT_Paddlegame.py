import numpy as np
import sounddevice as sd
import pygame

# Audio Config
SAMPLE_RATE = 44100  
DURATION = 0.1  

# Pygame Setup
WIDTH, HEIGHT = 800, 400
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BALL_COLOR = (255, 0, 0)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

class FrequencyPaddleGame:
    def __init__(self):
        self.buffer = np.zeros(int(SAMPLE_RATE * DURATION))
        self.paddle_y = HEIGHT // 2  # Start in the middle
        self.target_paddle_y = self.paddle_y  # For smoothing
        self.running = True

        # Ball properties
        self.ball_x = WIDTH // 2
        self.ball_y = HEIGHT // 2
        self.ball_dx = 4  # Ball speed in X direction
        self.ball_dy = 4  # Ball speed in Y direction
        self.ball_size = 10

        # Paddle properties
        self.paddle_x = 50
        self.paddle_width = 10
        self.paddle_height = 80

        # Start audio stream
        self.stream = sd.InputStream(callback=self.audio_callback, channels=1, samplerate=SAMPLE_RATE, blocksize=1024)
        self.stream.start()

    def audio_callback(self, indata, frames, time, status):
        if status:
            print(status)
        self.buffer = np.roll(self.buffer, -frames)
        self.buffer[-frames:] = indata[:, 0]

    def detect_frequency(self):
        """Process FFT and return the dominant frequency"""
        hann_window = np.hanning(len(self.buffer))
        fft_data = np.fft.rfft(self.buffer * hann_window)
        fft_magnitude = np.abs(fft_data)
        freqs = np.fft.rfftfreq(len(self.buffer), d=1 / SAMPLE_RATE)

        # Apply a minimum threshold to ignore silence or low noise
        if np.max(fft_magnitude) < 0.05:  # Adjust threshold as needed
            return 0

        peak_idx = np.argmax(fft_magnitude)
        detected_freq = freqs[peak_idx] if fft_magnitude[peak_idx] > 0 else 0
        return detected_freq

    def update_paddle(self):
        """Smoothly move the paddle based on detected frequency"""
        freq = self.detect_frequency()

        # Ignore very low frequencies
        min_freq, max_freq = 500, 3000  
        if freq > min_freq:
            normalized = np.clip((freq - min_freq) / (max_freq - min_freq), 0, 1)
            self.target_paddle_y = int(HEIGHT * (1 - normalized))  

        # Smooth movement (interpolation)
        self.paddle_y += (self.target_paddle_y - self.paddle_y) * 0.2  

    def update_ball(self):
        """Move the ball and handle collisions"""
        self.ball_x += self.ball_dx
        self.ball_y += self.ball_dy

        # Ball bounces off top and bottom
        if self.ball_y <= 0 or self.ball_y >= HEIGHT:
            self.ball_dy *= -1

        # Ball resets if it goes past the paddle (left side)
        if self.ball_x <= 0:
            self.ball_x = WIDTH // 2
            self.ball_y = HEIGHT // 2
            self.ball_dx *= -1  # Reverse direction

        # Ball bounces off the right wall
        if self.ball_x >= WIDTH:
            self.ball_x = WIDTH - self.ball_size  # Keep it inside screen
            self.ball_dx *= -1  # Reverse direction

        # Ball bounces off the paddle
        if (self.paddle_x < self.ball_x < self.paddle_x + self.paddle_width and
            self.paddle_y - self.paddle_height // 2 < self.ball_y < self.paddle_y + self.paddle_height // 2):
            self.ball_dx *= -1  # Bounce back

    def run(self):
        """Main game loop"""
        while self.running:
            screen.fill((0, 0, 0))

            self.update_paddle()
            self.update_ball()

            # Draw Paddle
            pygame.draw.rect(screen, GREEN, (self.paddle_x, self.paddle_y - self.paddle_height // 2, self.paddle_width, self.paddle_height))

            # Draw Ball
            pygame.draw.circle(screen, BALL_COLOR, (self.ball_x, self.ball_y), self.ball_size)

            # Event Handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            pygame.display.flip()
            clock.tick(30)

        self.stream.stop()
        self.stream.close()
        pygame.quit()

if __name__ == "__main__":
    game = FrequencyPaddleGame()
    game.run()
