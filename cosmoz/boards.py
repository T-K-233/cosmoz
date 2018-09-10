import time
import socket
from struct import pack

class Arduino_UNO:
    num_pins = [14, 6]

    def __init__(self, joysticks, communication='WLAN'):
        self.state = 0
        self.timer = time.time()
        self._communication = communication
        self._commands = []
        self._buffer = b''
        self._init_pins()
        self._init_joysticks(joysticks)
        self._init_socket()

    def _init_pins(self):
        self.pins = {}
        for i in range(self.num_pins[0]):
            self.pins[i] = [0, 0]
        for i in range(self.num_pins[1]):
            self.pins['A%d'%i] = [0, 0]

    def _init_joysticks(self, joysticks):
        self._joysticks = []
        if type(joysticks) == list:
            self._joysticks.extend(joysticks)
        else:
            self._joysticks.append(joysticks)

    def _init_socket(self):
        if self._communication:
            self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM,0)
            self._sock.bind(('0.0.0.0', 10001))
            self._sock.listen(1)
            self._conn, addr = self._sock.accept()
            self._conn.recv(8)
        self.state = 1
        self._conn.settimeout(0.5)
        print('Connected to board')
        

    def _check_state(self):
        for joy in self._joysticks:
            if not joy.state:
                self._conn.send(pack('BBBB', 128, 255, 255, 255))
                raise Exception('手柄断链！')
        return True

    def _refresh_joysticks(self):
        for joy in self._joysticks:
            joy.refresh()

    def analogWrite(self, pin, val):
        val = int(min(max(val, 0), 255))
        if not self.pins[pin] == val:
            self.pins[pin] = val
            self._buffer += pack('BBBB', 3, pin, val, 255)

    def digitalWrite(self, pin, val):
        val = 1 if val else 0
        if not self.pins[pin] == val:
            self.pins[pin] = val
            self._buffer += pack('BBBB', 5, pin, val, 255)
    
    def add_command(self, command_func):
        self.commands.append(command_func)
    
    def execute(self):
        if not self._check_state():
            raise Exception()
        if self._buffer and self._communication:
            try:
                self._conn.send(self._buffer)
                self._conn.recv(1)
            except ConnectionResetError or ConnectionAbortedError:
                print('disconnected, retrying connection')
                self._init_socket()
        self._buffer = b''
        self._refresh_joysticks()
        time.sleep(1 / 60.)
