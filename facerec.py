import pygame
from pygame.locals import *
import cv2
import numpy as np
import sys

pygame.init()
pygame.display.set_caption("OpenCV camera stream on Pygame")
screen = pygame.display.set_mode([1280,720])
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

class Camera:
    def __init__(self):
        self.camera = cv2.VideoCapture(0)
        self.ret, self.image = self.camera.read()
        self.ccolor = [0,0,0]
        self.faces = []

    def calibrate(self):
        crect = pygame.draw.rect(screen, (255,0,0), (145,105,30,30), 4)
        self.ccolor = pygame.transform.average_color(self.image, crect)
        screen.fill(self.ccolor, (0,0,50,50))
        pygame.display.flip()

    def capture_frame(self, to_gray=False):
        self.ret, frame = self.camera.read()
        if not self.ret:
            return None
        if to_gray:
            return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        return frame

    def detect_faces(self):
        frame = self.capture_frame()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        self.faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in self.faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 255, 0), 2)
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = frame[y:y+h, x:x+w]
            
            eyes = eye_cascade.detectMultiScale(roi_gray)
            for (ex, ey, ew, eh) in eyes:
                cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (0, 127, 255), 2)

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = np.rot90(frame)
        self.image = pygame.surfarray.make_surface(frame)

    def update_flip(self, pos):
        screen.blit(self.image, pos)

    def shutdown(self):
        self.camera.release()

camera = Camera()

try:
    while True:
        screen.fill([0,0,0])
        camera.detect_faces()
        camera.update_flip((0,0))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit(0)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            camera.calibrate()

except (KeyboardInterrupt, SystemExit):
    pygame.quit()
    camera.shutdown()
    cv2.destroyAllWindows()
