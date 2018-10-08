from cosmoz.boards import Arduino_UNO
from cosmoz.joysticks import XBoxController
from cosmoz.modules import tank_drive

from struct import pack


joysticks = XBoxController.init_all()
joystick_0 = joysticks[0]

board = Arduino_UNO(joystick_0)

while True:
    tank_drive(board, 5, 7, 6, 8, joystick_0)
    if joystick_0.button[12]:
        board._buffer += pack('BBBB', 12, 3, 15, 255)
    else:
        board._buffer += pack('BBBB', 12, 3, 1, 255)
    # print(joystick_0.button)
    board.execute()
