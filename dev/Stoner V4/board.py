import socket

class Arduino_UNO:
    pin_num = [14, 6]

    def __init__(self, joysticks, conn_type=''):
        self._init_pins()
        self._init_joystick(joysticks)
        self._init_communication()
        self.commands = []

    def _init_pins(self):
        self.pins = {}
        for dP in range(pin_num[0]):
            self.pins[dP] = (0, 0)
        for aP in range(pin_num[1]):
            self.pins['A%d' % aP] = (0, 0)

    def _init_joystick(self, joysticks):
        self.joysticks = []
        if type(joysticks) is list:
            self.joysticks.extend(j for j in joysticks)
        else:
            self.joysticks.append(joysticks)
        
    def _init_communication(self):
        pass
         # TODO!

    def analogWrite(self, pin, val):
        if self.pins['A%d' % pin] != val:
            self.commands.append((3, pin, val, 255))

    def digitalWrite(self, pin, val):
        if self.pins[pin] != val:
            self.commands.append((5, pin, val, 255))
    
    def execute(self):
        for joy in self.joysticks:
            if joy.state == 0:
                raise Exception('joystick not connected')
