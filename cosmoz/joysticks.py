'''
Adapted from Xbox-360-Controller-for-Python
https://github.com/r4dian/Xbox-360-Controller-for-Python
Modified by -T.K.- Aug 2018
'''
import ctypes
import time
import sys
from operator import itemgetter, attrgetter
from itertools import count, starmap
from pyglet import event

class XINPUT_GAMEPAD(ctypes.Structure):
    _fields_ = [
        ('buttons', ctypes.c_ushort),  # wButtons
        ('4', ctypes.c_ubyte),  # bLeftTrigger
        ('5', ctypes.c_ubyte),  # bLeftTrigger
        ('0', ctypes.c_short),  # sThumbLX
        ('1', ctypes.c_short),  # sThumbLY
        ('2', ctypes.c_short),  # sThumbRx
        ('3', ctypes.c_short),  # sThumbRy
    ]

class XINPUT_STATE(ctypes.Structure):
    _fields_ = [
        ('packet_number', ctypes.c_ulong),  # dwPacketNumber
        ('gamepad', XINPUT_GAMEPAD),  # Gamepad
    ]

class XINPUT_VIBRATION(ctypes.Structure):
    _fields_ = [("l_motor", ctypes.c_ushort),
                ("r_motor", ctypes.c_ushort)]

class XINPUT_BATTERY_INFORMATION(ctypes.Structure):
    _fields_ = [("BatteryType", ctypes.c_ubyte),
                ("BatteryLevel", ctypes.c_ubyte)]

xinput = ctypes.windll.xinput1_4


def struct_dict(struct):
    '''
    take a ctypes.Structure and return its field/value pairs as a dict.
    >>> 'buttons' in struct_dict(XINPUT_GAMEPAD)
    True
    >>> struct_dict(XINPUT_GAMEPAD)['buttons'].__class__.__name__
    'CField'
    '''
    get_pair = lambda field_type: (
        field_type[0], getattr(struct, field_type[0]))
    return dict(list(map(get_pair, struct._fields_)))

def get_bit_values(number, size=32):
    '''
    Get bit values as a list for a given number
    >>> get_bit_values(1) == [0]*31 + [1]
    True
    >>> get_bit_values(0xDEADBEEF)
    [1L, 1L, 0L, 1L, 1L, 1L, 1L, 0L, 1L, 0L, 1L, 0L, 1L, 1L, 0L, 1L, 1L, 0L, 1L, 1L, 1L, 1L, 1L, 0L, 1L, 1L, 1L, 0L, 1L, 1L, 1L, 1L]
    You may override the default word size of 32-bits to match your actual
    application.
    >>> get_bit_values(0x3, 2)
    [1L, 1L]
    >>> get_bit_values(0x3, 4)
    [0L, 0L, 1L, 1L]
    '''
    res = list(gen_bit_values(number))
    res.reverse()
    # 0-pad the most significant bit
    res = [0] * (size - len(res)) + res
    return res

def gen_bit_values(number):
    '''
    Return a zero or one for each bit of a numeric value up to the most significant 1 bit, beginning with the least significant bit.
    '''
    number = int(number)
    while number:
        yield number & 0x1
        number >>= 1


class XBoxController(event.EventDispatcher):
    '''
    A stateful wrapper, using pyglet event model, that binds to one XInput device and dispatches events when states change.
    '''
    max_devices = 4

    def __init__(self, device_number, normalize_axes=True):
        self.device_number = device_number
        values = vars()
        del values['self']
        self.__dict__.update(values)
        super(XBoxController, self).__init__()
        self._last_state = self.get_state()
        self.axis = [0.0] * 6
        self.button = [0] * 16
        # Set the method that will be called to normalize the values for analog axis.
        choices = [self.translate_identity, self.translate_using_data_size]
        self.translate = choices[normalize_axes]
        self.get_state()

    def translate_using_data_size(self, value, data_size):
        # normalizes analog data to [0,1] for unsigned data and [-0.5,0.5] for signed data
        data_bits = 8 * data_size
        return float(value) / (2 ** data_bits - 1)

    def translate_identity(self, value, data_size=None):
        return value

    def get_state(self):
        'Get the state of the controller represented by this object'
        state = XINPUT_STATE()
        res = xinput.XInputGetState(self.device_number, ctypes.byref(state))
        if res == 0:            # SUCCESS
            self.state = 1
            return state
        if res == 1167:         # DEVICE_NOT_CONNECTED
            self.state = 0
        else:
            raise RuntimeError('Unknown error %d attempting to get state of device %d' % (res, self.device_number))

    def is_connected(self):
        return self._last_state is not None

    def set_vibration(self, left_motor, right_motor):
        'Control the speed of both motors seperately'
        XInputSetState = xinput.XInputSetState
        XInputSetState.argtypes = [ctypes.c_uint, ctypes.POINTER(XINPUT_VIBRATION)]
        XInputSetState.restype = ctypes.c_uint

        vibration = XINPUT_VIBRATION(int(left_motor * 65535), int(right_motor * 65535))
        XInputSetState(self.device_number, ctypes.byref(vibration))

    def get_battery_information(self):
        'Get battery type & charge level'
        BATTERY_DEVTYPE_GAMEPAD = 0x00
        BATTERY_DEVTYPE_HEADSET = 0x01
        XInputGetBatteryInformation = xinput.XInputGetBatteryInformation
        XInputGetBatteryInformation.argtypes = [ctypes.c_uint, ctypes.c_ubyte, ctypes.POINTER(XINPUT_BATTERY_INFORMATION)]
        XInputGetBatteryInformation.restype = ctypes.c_uint 

        battery = XINPUT_BATTERY_INFORMATION(0,0)
        XInputGetBatteryInformation(self.device_number, BATTERY_DEVTYPE_GAMEPAD, ctypes.byref(battery))
        '''
        define BATTERY_TYPE_DISCONNECTED       0x00
        define BATTERY_TYPE_WIRED              0x01
        define BATTERY_TYPE_ALKALINE           0x02
        define BATTERY_TYPE_NIMH               0x03
        define BATTERY_TYPE_UNKNOWN            0xFF
        define BATTERY_LEVEL_EMPTY             0x00
        define BATTERY_LEVEL_LOW               0x01
        define BATTERY_LEVEL_MEDIUM            0x02
        define BATTERY_LEVEL_FULL              0x03
        '''
        batt_type = 'Unknown' if battery.BatteryType == 0xFF else ['Disconnected', 'Wired', 'Alkaline', 'Nimh'][battery.BatteryType]
        level = ['Empty', 'Low', 'Medium', 'Full'][battery.BatteryLevel]
        return batt_type, level

    def handle_changed_state(self, state):
        'Dispatch various events as a result of the state changing'
        self.dispatch_event('on_state_changed', state)
        self.dispatch_axis_events(state)
        self.dispatch_button_events(state)

    def dispatch_axis_events(self, state):
        axis_fields = dict(XINPUT_GAMEPAD._fields_)
        axis_fields.pop('buttons')
        for axis, type in list(axis_fields.items()):
            old_val = getattr(self._last_state.gamepad, axis)
            new_val = getattr(state.gamepad, axis)
            data_size = ctypes.sizeof(type)
            old_val = self.translate(old_val, data_size)
            new_val = self.translate(new_val, data_size)
            # an attempt to add deadzones and dampen noise
            if ((old_val!=new_val and (new_val>0.08000000000000000 or new_val<-0.08000000000000000) and abs(old_val-new_val) > 0.00000000500000000) or (axis=='4' or axis=='5') and new_val==0 and abs(old_val-new_val) > 0.00000000500000000):
                self.dispatch_event('on_axis', axis, new_val)

    def dispatch_button_events(self, state):
        changed = state.gamepad.buttons ^ self._last_state.gamepad.buttons
        changed = get_bit_values(changed, 16)
        buttons_state = get_bit_values(state.gamepad.buttons, 16)
        changed.reverse()
        buttons_state.reverse()
        button_numbers = count(1)
        changed_buttons = list(filter(itemgetter(0), list(zip(changed, button_numbers, buttons_state))))
        tuple(starmap(self.dispatch_button_event, changed_buttons))

    def dispatch_button_event(self, changed, number, pressed):
        self.dispatch_event('on_button', number-1, pressed)     # -1 to restore index to 0

    def on_axis(self, axis, value):
        self.axis[int(axis)] = value * 2

    def on_button(self, button, pressed):
        self.button[button] = pressed
    
    def refresh(self):
        state = self.get_state()
        try:
            if state.packet_number != self._last_state.packet_number:
                self.handle_changed_state(state)
        except:
            pass
        self._last_state = state

    @staticmethod
    def init_all():
        devices = list(map(XBoxController, list(range(XBoxController.max_devices))))
        devices = [d for d in devices if d.is_connected()]
        print('%d joysticks found.' % len(devices))
        return devices

list(map(XBoxController.register_event_type, [
    'on_state_changed',
    'on_axis',
    'on_button',
]))








import keyboard

class Keyboard:
    def __init__(self, suppress=False):
        self.keys = []
        self.state = 1
        self._suppress = suppress

    def _process_keys(self, e):
        if e.event_type == 'down':
            e = e.scan_code
            if e not in self.keys:
                self.keys.append(e)
        elif e.event_type == 'up':
            e = e.scan_code
            if e in self.keys:
                self.keys.remove(e)

    def key(self, key):
        if type(key) == int:
            return key in self.keys

    def refresh(self):
        keyboard.hook(self._process_keys, suppress=self._suppress)

