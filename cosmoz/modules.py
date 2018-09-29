from .signals import HIGH, LOW


def motor_control(board, analogPin, digitalPin, value, threshold=.2):
    '''
    control a motor using the L298 controller.

    @param board: a board object from <cosmoz.boards>. 
    @param analogPin: an analog pin for the L298 controller. 
    @param digitalPin: a digital pin for the L298 controller. 
    @param value: the speed of the motor, negative for counterclockwise. 
    @param threshold: the responsive to <value>. Defaults to 0.2.
    '''
    if value > threshold:
        board.analogWrite(analogPin, value * 254)
        board.digitalWrite(digitalPin, LOW)
    elif value < -threshold:
        board.analogWrite(analogPin, -value * 254)
        board.digitalWrite(digitalPin, HIGH)
    else:
        board.digitalWrite(digitalPin, LOW)
        board.digitalWrite(analogPin, LOW)

def motor_control_2(board, analogPin, digitalPin, value, threshold=.2):
    '''
    control a motor using the L298 controller.

    @param board: a board object from <cosmoz.boards>. 
    @param analogPin: an analog pin for the L298 controller. 
    @param digitalPin: a digital pin for the L298 controller. 
    @param value: the speed of the motor, negative for counterclockwise. 
    @param threshold: the responsive to <value>. Defaults to 0.2.
    '''
    if value > threshold:
        board.analogWrite(analogPin, value * 254)
        board.digitalWrite(digitalPin, LOW)
    elif value < -threshold:
        board.analogWrite(analogPin, (1+value) * 254)
        board.digitalWrite(digitalPin, HIGH)
    else:
        board.digitalWrite(digitalPin, LOW)
        board.digitalWrite(analogPin, LOW)

def tank_drive(board, leftAnalogPin, leftDigitalPin, rightAnalogPin, rightDigitalPin, joystick):
    '''
    drives a robot using tank controlling. 

    @param board: a board object from <cosmoz.boards>. 
    @param leftAnalogPin: the analog pin used for the left motor. 
    @param leftDigitalPin: the digital pin used for the left motor.
    @param rightAnalogPin: don't want to repeat.... i think you will get it. 
    @param rightDigitalPin: same as above.....
    @param joystick: a joystick object from <cosmoz.joysticks>. 
    '''
    motor_control(board, leftAnalogPin, leftDigitalPin, joystick.axis[1])
    motor_control(board, rightAnalogPin, rightDigitalPin, joystick.axis[3])

def keyboard_drive(board, leftAnalogPin, leftDigitalPin, rightAnalogPin, rightDigitalPin, keyboard, throttle=0.6):
    '''
    W: 17
    A: 30
    D: 32
    S: 31
    '''
    if keyboard.key(17):
        if keyboard.key(30):
            motor_control(board, leftAnalogPin, leftDigitalPin, 0.4*throttle)
            motor_control(board, rightAnalogPin, rightDigitalPin, throttle)
        elif keyboard.key(32):
            motor_control(board, leftAnalogPin, leftDigitalPin, throttle)
            motor_control(board, rightAnalogPin, rightDigitalPin, 0.4*throttle)
        else:
            motor_control(board, leftAnalogPin, leftDigitalPin, throttle)
            motor_control(board, rightAnalogPin, rightDigitalPin, throttle)
    elif keyboard.key(31):
        if keyboard.key(30):
            motor_control(board, leftAnalogPin, leftDigitalPin, -0.4*throttle)
            motor_control(board, rightAnalogPin, rightDigitalPin, -throttle)
        elif keyboard.key(32):
            motor_control(board, leftAnalogPin, leftDigitalPin, -throttle)
            motor_control(board, rightAnalogPin, rightDigitalPin, -0.4*throttle)
        else:
            motor_control(board, leftAnalogPin, leftDigitalPin, -throttle)
            motor_control(board, rightAnalogPin, rightDigitalPin, -throttle)
    elif keyboard.key(30):
        motor_control(board, leftAnalogPin, leftDigitalPin, -0.8*throttle)
        motor_control(board, rightAnalogPin, rightDigitalPin, 0.8*throttle)
    elif keyboard.key(32):
        motor_control(board, leftAnalogPin, leftDigitalPin, 0.8*throttle)
        motor_control(board, rightAnalogPin, rightDigitalPin, -0.8*throttle)
    else:
        motor_control(board, leftAnalogPin, leftDigitalPin, 0)
        motor_control(board, rightAnalogPin, rightDigitalPin, 0)
