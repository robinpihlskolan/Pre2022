import pygame
import serial
import time

# Initialize Pygame
pygame.init()


serial_port = serial.Serial('COM3', 9600) 
time.sleep(2)

# Map values function
def map_value(value, from_min, from_max, to_min, to_max):
    """Map a value from one range to another."""
    return int((value - from_min) * (to_max - to_min) / (from_max - from_min) + to_min)


servo_angle = 90 

try:
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                  
                    servo_angle -= 10
                    if servo_angle < 0:
                        servo_angle = 0
                elif event.key == pygame.K_d:
                    
                    servo_angle += 10
                    if servo_angle > 180:
                        servo_angle = 180
                
                # Send servo angle to Arduino
                serial_port.write(bytes([servo_angle]))
                time.sleep(0.1)  

except KeyboardInterrupt:
    # Exit the program
    pygame.quit()
    serial_port.close()
