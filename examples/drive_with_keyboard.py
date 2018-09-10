from cosmoz.boards import Arduino_UNO
from cosmoz.joysticks import Keyboard
from cosmoz.modules import keyboard_drive


keyboard = Keyboard(suppress=True)
board = Arduino_UNO(keyboard)

while True:
    keyboard_drive(board, 6, 8, 5, 7, keyboard, throttle=0.7)
    board.execute()
