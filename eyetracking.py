import cv2
import numpy as np
import pygame
import dlib
from imutils import face_utils

# Initialize Pygame and display
pygame.init()
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("Eye Tracking")
font = pygame.font.Font(None, 36)

# Load dlib face detector and landmark predictor
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

# Define eye region
LEFT_EYE = list(range(36, 42))
RIGHT_EYE = list(range(42, 48))

# Function to get eye direction
def get_eye_direction(landmarks):
    # Get the center positions of both eyes
    left_eye = landmarks[LEFT_EYE]
    right_eye = landmarks[RIGHT_EYE]

    left_center = np.mean(left_eye, axis=0)
    right_center = np.mean(right_eye, axis=0)

    # Calculate the average horizontal position of both eyes
    eye_center = (left_center[0] + right_center[0]) / 2

    # Calculate the center of the face (roughly in the middle of the frame)
    frame_center = 320  # Half of 640 (frame width)

    # Determine the eye's direction
    if eye_center < frame_center - 10:  # Looking left
        return "Looking Left"
    elif eye_center > frame_center + 10:  # Looking right
        return "Looking Right"
    else:  # Looking center
        return "Looking Center"

# Initialize webcam
cap = cv2.VideoCapture(0)

while True:
    # Capture frame from webcam
    ret, frame = cap.read()

    if not ret:
        break

    # Convert to grayscale for face detection
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces
    faces = detector(gray)

    # Process faces and landmarks
    for face in faces:
        shape = predictor(gray, face)
        shape = face_utils.shape_to_np(shape)

        # Get the eye direction
        eye_direction = get_eye_direction(shape)

        # Flip the image to create the mirror effect (only for display)
        frame_flipped = frame
    

        # Draw the landmarks (green dots) on the flipped frame
        for (x, y) in shape:
            cv2.circle(frame_flipped, (x, y), 1, (0, 255, 0), -1)

       

        # Convert the flipped frame to RGB for Pygame
        frame_flipped = cv2.cvtColor(frame_flipped, cv2.COLOR_BGR2RGB)

        # Rotate the frame 90 degrees before showing in Pygame
        frame_flipped = np.rot90(frame_flipped)

        # Create a Pygame surface from the numpy array
        frame_flipped_surface = pygame.surfarray.make_surface(frame_flipped)

        # Draw the text on the flipped frame using Pygame (this is the final step)
        text_surface = font.render(eye_direction, True, (255, 255, 0))  # Yellow text
        screen.blit(frame_flipped_surface, (0, 0))  # Blit the flipped image first
        screen.blit(text_surface, (50, 50))  # Draw text at the desired position

    # Display the frame
    pygame.display.flip()

    # Handle events (to quit the program)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            cap.release()
            pygame.quit()
            quit()
