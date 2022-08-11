import bthid
import time
from machine import Pin
from bthid import Joystick


class Device:
    def __init__(self):
        self.joystick = Joystick("guitar")
        self.buttons = {
            "GREEN": (Pin(23, Pin.IN), self.button_green),
            "RED": (Pin(22, Pin.IN), self.button_red),
            "YELLOW": (Pin(21, Pin.IN), self.button_yellow),
            "BLUE": (Pin(19, Pin.IN), self.button_blue),
            "ORANGE": (Pin(18, Pin.IN), self.button_orange),
            "START": (Pin(17, Pin.IN), self.button_start),
            "SELECT": (Pin(16, Pin.IN), self.button_select)
        }
        self.joystick.set_state_change_callback(self.joystick_state_callback)
        self.joystick.start()
        pass

    def joystick_state_callback(self):
        if self.joystick.get_state() is Joystick.DEVICE_IDLE:
            return
        elif self.joystick.get_state() is Joystick.DEVICE_ADVERTISING:
            return
        elif self.joystick.get_state() is Joystick.DEVICE_CONNECTED:
            return
        else:
            return

    def advertise(self):
        self.joystick.start_advertising()

    def stop_advertising(self):
        self.joystick.stop_advertising()

    def button_green(self, val):
        self.joystick.set_buttons(b1=val)
        self.joystick.notify_hid_report()

    def button_red(self, val):
        self.joystick.set_buttons(b2=val)
        self.joystick.notify_hid_report()

    def button_yellow(self, val):
        self.joystick.set_buttons(b3=val)
        self.joystick.notify_hid_report()

    def button_blue(self, val):
        self.joystick.set_buttons(b4=val)
        self.joystick.notify_hid_report()

    def button_orange(self, val):
        self.joystick.set_buttons(b5=val)
        self.joystick.notify_hid_report()

    def button_start(self, val):
        self.joystick.set_buttons(b6=val)
        self.joystick.notify_hid_report()

    def button_select(self, val):
        self.joystick.set_buttons(b7=val)
        self.joystick.notify_hid_report()

    def start(self):
        self.joystick.start_advertising()
        while True:
            self.buttons["GREEN"][0].value()


if __name__ == "__main__":
    d = Device()
    d.start()