import pygame
import requests
import time
import arduino
from arduino.signal import *


board = arduino.board.Arduino_UNO(method=arduino.connection.WLAN, url="http://192.168.1.177")

THRESHOLD = 60

config_joystick = True


pygame.init()
screen = pygame.display.set_mode((640, 360))

if config_joystick:
    pass
    pygame.joystick.init()
    joystick = pygame.joystick.Joystick(0)
    joystick.init()


pygame.time.delay(4)


print('='*24+' Ready '+'='*24)


background = pygame.image.load('standard.png')

clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit();      #sys.exit() if sys is imported

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                board.digitalWrite(7, LOW)
                board.analogWrite(5, 160)
                board.digitalWrite(8, LOW)
                board.analogWrite(6, 160)
            elif event.key == pygame.K_a:
                board.digitalWrite(7, LOW)
                board.analogWrite(5, 0)
                board.digitalWrite(8, LOW)
                board.analogWrite(6, 160)
            elif event.key == pygame.K_d:
                board.digitalWrite(7, LOW)
                board.analogWrite(5, 160)
                board.digitalWrite(8, LOW)
                board.analogWrite(6, 0)
            elif event.key == pygame.K_s:
                board.digitalWrite(7, HIGH)
                board.analogWrite(5, 120)
                board.digitalWrite(8, HIGH)
                board.analogWrite(6, 120)
            elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                pygame.quit()
                board.EMERGENCYSTOP()
    
        if event.type == pygame.JOYAXISMOTION:
            if event.axis == 1:
                left = int(event.value * 150)
                if left > THRESHOLD:
                    board.digitalWrite(7, LOW)
                    board.analogWrite(5, left)
                elif left < -THRESHOLD:
                    board.digitalWrite(7, HIGH)
                    board.analogWrite(5, 255 + left)
                else:
                    board.digitalWrite(7, LOW)
                    board.analogWrite(5, 0)

            if event.axis == 3:
                right = int(event.value * 150)
                if right > THRESHOLD:
                    board.digitalWrite(8, LOW)
                    board.analogWrite(6, right)
                elif right < -THRESHOLD:
                    board.digitalWrite(8, HIGH)
                    board.analogWrite(6, 255 + right)
                else:
                    board.digitalWrite(8, LOW)
                    board.analogWrite(6, 0)
    
    screen.blit(background, (0, 0))
    pygame.display.flip()
    clock.tick(30)
