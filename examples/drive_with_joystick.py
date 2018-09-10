from cosmoz.boards import Arduino_UNO
from cosmoz.joysticks import XBoxController
from cosmoz.modules import tank_drive


joysticks = XBoxController.init_all()
joystick_0 = joysticks[0]

board = Arduino_UNO(joystick_0)

while True:
    tank_drive(board, 6, 8, 5, 7, joystick_0)
    board.execute()
