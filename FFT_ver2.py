import numpy as np
import sounddevice as sd
import pygame

class AudioProcessor:
    SAMPLE_RATE = 44100  # Hz
    DURATION = 0.1  # seconds
    N_SAMPLES = int(SAMPLE_RATE * DURATION)
    WHISTLE_MIN_FREQ = 1000  # Hz
    WHISTLE_MAX_FREQ = 40000  # Hz

    def __init__(self):
        self.buffer = np.zeros(self.N_SAMPLES)

        self.stream = sd.InputStream(
            callback=self.audio_callback, channels=1,
            samplerate=self.SAMPLE_RATE, blocksize=1024
        )
        self.stream.start()

    def audio_callback(self, indata, frames, time, status):
        if status:
            print(status)
        self.buffer = np.roll(self.buffer, -frames, axis=0)
        self.buffer[-frames:] = indata[:, 0]  # Use only one channel

    def get_fft_data(self):
        hann_window = np.hanning(len(self.buffer))
        fft_data = np.fft.rfft(self.buffer * hann_window)
        fft_magnitude = np.abs(fft_data)
        freqs = np.fft.rfftfreq(len(self.buffer), d=1/self.SAMPLE_RATE)

        # Apply filters
        fft_magnitude[freqs < self.WHISTLE_MIN_FREQ] = 0
        fft_magnitude[freqs > self.WHISTLE_MAX_FREQ] = 0

        # Reduce low-frequency noise
        fft_magnitude[fft_magnitude < np.max(fft_magnitude) * 0.1] = 0

        # Normalize
        max_val = np.max(fft_magnitude)
        if max_val > 0:
            fft_magnitude *= 1 / max_val  # Normalize
        else:
            fft_magnitude[:] = 0  # Avoid NaN issues

        return freqs, fft_magnitude

    def stop(self):
        self.stream.stop()
        self.stream.close()


class WhistleDetector:
    NOTE_NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

    @staticmethod
    def freq_to_note(freq):
        if freq <= 0:
            return "-"

        A4 = 440.0  # Reference frequency
        C0 = A4 * 2**(-4.75)  # Calculate C0 (first musical C)

        n = round(12 * np.log2(freq / C0))  # Total semitone index from C0

        note = WhistleDetector.NOTE_NAMES[n % 12]  # Get note name
        octave = (n // 12)  # Correct octave calculation

        return f"{note}{octave}"



    def detect_peak(self, freqs, fft_magnitude):
        """ Detects the peak frequency and converts it to a musical note. """
        if len(freqs) == 0 or len(fft_magnitude) == 0:
            return 0, "-"

        peak_idx = np.argmax(fft_magnitude)
        detected_freq = freqs[peak_idx] if np.max(fft_magnitude) > 0 else 0
        detected_note = self.freq_to_note(detected_freq)
        return detected_freq, detected_note


    


class Visualizer:
    WIDTH, HEIGHT = 800, 400

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Whistle Detector and FFT")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)

    def draw(self, fft_magnitude, freqs, detected_freq, detected_note):
        self.screen.fill((0, 0, 0))

        # Scale FFT to fit screen width
        num_bins = len(fft_magnitude)
        step = max(1, num_bins // self.WIDTH)
        scaled_fft = fft_magnitude[:self.WIDTH * step:step] * self.HEIGHT

        # Draw FFT bars
        for x in range(len(scaled_fft)):
            pygame.draw.line(self.screen, (0, 255, 0), (x, self.HEIGHT), (x, self.HEIGHT - int(scaled_fft[x])), 1)

        # Display detected frequency and note
        text_surface = self.font.render(f"Freq: {detected_freq:.1f} Hz  Note: {detected_note}", True, (255, 255, 255))
        self.screen.blit(text_surface, (20, 20))

        pygame.display.flip()
        self.clock.tick(30)

    def close(self):
        pygame.quit()


class MainApp:
    def __init__(self):
        self.audio_processor = AudioProcessor()
        self.detector = WhistleDetector()
        self.visualizer = Visualizer()
        self.running = True

    def run(self):
        while self.running:
            freqs, fft_magnitude = self.audio_processor.get_fft_data()
            detected_freq, detected_note = self.detector.detect_peak(freqs, fft_magnitude)
            self.visualizer.draw(fft_magnitude, freqs, detected_freq, detected_note)

            # Handle Pygame events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

        self.audio_processor.stop()
        self.visualizer.close()


if __name__ == "__main__":
    app = MainApp()
    app.run()
