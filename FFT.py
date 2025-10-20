import numpy as np
import sounddevice as sd
import pygame



# Audio configuration
SAMPLE_RATE = 44100  # Hz
DURATION = 0.1  # seconds
N_SAMPLES = int(SAMPLE_RATE * DURATION)

# Frequency range for whistles
WHISTLE_MIN_FREQ = 1000  # Hz
WHISTLE_MAX_FREQ = 40000  # Hz

# Pygame setup
WIDTH, HEIGHT = 800, 400
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Whistle Detector and FFT")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

# Capture audio
buffer = np.zeros(N_SAMPLES)
def audio_callback(indata, frames, time, status):
    global buffer
    if status:
        print(status)
    buffer = np.roll(buffer, -frames, axis=0)
    buffer[-frames:] = indata[:, 0]  # Use only one channel

stream = sd.InputStream(callback=audio_callback, channels=1, samplerate=SAMPLE_RATE, blocksize=1024)
stream.start()

def freq_to_note(freq):
    if freq <= 0:
        return "-"
    A4 = 440.0
    semitone_ratio = 2 ** (1 / 12)
    note_names = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
    n = round(12 * np.log2(freq / A4))
    octave = 4 + (n // 12)
    note = note_names[n % 12]
    return f"{note}{octave}"

running = True
while running:
    screen.fill((0, 0, 0))
    
    # Process FFT
    hann_window = np.hanning(len(buffer))
    fft_data = np.fft.rfft(buffer * hann_window)
    fft_magnitude = np.abs(fft_data)
    freqs = np.fft.rfftfreq(len(buffer), d=1/SAMPLE_RATE)
    
    # Apply high-pass filter
    fft_magnitude[freqs < WHISTLE_MIN_FREQ] = 0
    fft_magnitude[freqs > WHISTLE_MAX_FREQ] = 0
    
    # Reduce low-frequency noise by zeroing out small values
    fft_magnitude[fft_magnitude < np.max(fft_magnitude) * 0.1] = 0
    
    # Normalize
    max_val = np.max(fft_magnitude)
    if max_val > 0:
        fft_magnitude *= HEIGHT / max_val  # Normalize
    else:
        fft_magnitude[:] = 0  # Avoid NaN issues
    
    # Detect dominant whistle frequency
    peak_idx = np.argmax(fft_magnitude)
    detected_freq = freqs[peak_idx] if max_val > 0 else 0
    detected_note = freq_to_note(detected_freq)
    
    # Scale FFT to fit screen width
    num_bins = len(fft_magnitude)
    step = max(1, num_bins // WIDTH)
    scaled_fft = fft_magnitude[:WIDTH * step:step]  # Downsample for display
    
    # Draw FFT bars
    for x in range(len(scaled_fft)):
        pygame.draw.line(screen, (0, 255, 0), (x, HEIGHT), (x, HEIGHT - int(scaled_fft[x])), 1)
    
    # Display detected frequency and note
    text_surface = font.render(f"Freq: {detected_freq:.1f} Hz  Note: {detected_note}", True, (255, 255, 255))
    screen.blit(text_surface, (20, 20))
    
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    pygame.display.flip()
    clock.tick(30)

stream.stop()
stream.close()
pygame.quit()
