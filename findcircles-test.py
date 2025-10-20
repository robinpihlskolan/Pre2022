import cv2
import numpy as np

# Load image, grayscale, Otsu's threshold
image = cv2.imread('stars.jpg')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

# Find circles with HoughCircles
circles = cv2.HoughCircles(thresh, cv2.HOUGH_GRADIENT, 1, minDist=2, param1=250, param2=1.2, minRadius=1, maxRadius=5)

print(circles[0, :])
print(len(circles[0,:]))
# Draw circles
if circles is not None:
    circles = np.round(circles[0, :]).astype("int")
    for (x,y,r) in circles:
        cv2.circle(image, (x,y), r, (36,255,12), 1)

print(circles[0, :])

cv2.imshow('thresh', thresh)
cv2.imshow('image', image)
cv2.waitKey()
