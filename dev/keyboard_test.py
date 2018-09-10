"""
Prints the scan code of all currently pressed keys.
Updates on every keyboard event.
"""
import keyboard
import time

keys = []

def print_pressed_keys(e):
    print(e.name, e.scan_code)


while True:
    keyboard.hook(print_pressed_keys)
    
