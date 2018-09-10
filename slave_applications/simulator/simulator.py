import socket
import time
from struct import pack, unpack

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.uix.floatlayout import FloatLayout

token = '00010205'

class Screen(FloatLayout):
    def __init__(self,**kwargs):
        super(Screen,self).__init__(**kwargs)
        self.add_widget(Image(source='arduino.png', size_hint=(.8, .8), pos_hint={'x':0, 'y':.1}))
        self.pin_num = 14
        self.pins = []
        self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM,0)
        self.sock.connect(('127.0.0.1', 10001))
        for i in range(self.pin_num):
            pin = Label(text='0', size_hint=(.1, .1), pos_hint={'x':.58, 'y':.029*i+.1}, halign='left')
            pin.val = 0
            self.pins.append(pin)
            self.add_widget(pin)
    
    def update(self, dt):
        streaming = True
        cmd = ''
        while streaming:
            self.sock.settimeout(.01)
            try:
                cmd = unpack('BBBB', self.sock.recv(4))
                self.pins[cmd[1]].val = cmd[2]
            except:
                streaming = False
            print(cmd)
        for char in token:
            self.sock.send(pack('B', int(char)))
        for pin in self.pins:
            pin.text = str(pin.val)

class SimulatorApp(App):
    def build(self):
        screen = Screen()
        Clock.schedule_interval(screen.update, 1 / 120.)
        return screen

if __name__ == '__main__':
    SimulatorApp().run()




