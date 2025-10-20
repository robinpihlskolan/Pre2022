import cv2
import dlib
import numpy as np
from imutils import face_utils

# Load face detector and landmark predictor
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

# Ideal ratio based on studies (eye-to-face width)
IDEAL_RATIO = 0.46

# Start webcam
cap = cv2.VideoCapture(0)

def distance(a, b):
    return np.linalg.norm(a - b)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Flip the frame horizontally for mirror effect
    frame = cv2.flip(frame, 1)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = detector(gray)

    for face in faces:
        shape = predictor(gray, face)
        shape = face_utils.shape_to_np(shape)

        # Get key points
        left_eye_outer = shape[36]
        right_eye_outer = shape[45]
        left_face = shape[0]
        right_face = shape[16]

        # Draw landmarks (eyes and face edges)
        for i in [36, 45, 0, 16, 30, 48, 54]:
            cv2.circle(frame, tuple(shape[i]), 2, (0, 255, 0), -1)

        # Measure distances
        eye_distance = distance(left_eye_outer, right_eye_outer)
        face_width = distance(left_face, right_face)

        # Calculate ratio
        if face_width > 0:
            ratio = eye_distance / face_width
            diff = abs(IDEAL_RATIO - ratio)

            # Score based on how close to ideal
            score = max(0, 100 - int(diff * 1000))  # Crude scoring system

            # Display text
            cv2.putText(frame, f"Eye/Face Ratio: {ratio:.2f}", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
            cv2.putText(frame, f"Beauty Score: {score}", (10, 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)

    cv2.imshow("Facial Ratio Analyzer", frame)

    if cv2.waitKey(1) & 0xFF == 27:  # ESC to exit
        break

cap.release()
cv2.destroyAllWindows()
