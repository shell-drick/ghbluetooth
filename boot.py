import time
import gc
from machine import Pin, ADC, PWM
from bthid import Joystick


class Device:
    def __init__(self):
        self.joystick = Joystick("guitar")
        self.joystick.load_secrets()
        self.buttons = [
            # Green
            Pin(21, Pin.IN, Pin.PULL_UP),
            # Red (broken)
            Pin(23, Pin.IN, Pin.PULL_UP),
            # Yellow
            Pin(18, Pin.IN, Pin.PULL_UP),
            # Blue
            Pin(19, Pin.IN, Pin.PULL_UP),
            # Orange
            Pin(22, Pin.IN, Pin.PULL_UP),
            # Start
            Pin(17, Pin.IN, Pin.PULL_UP),
            # Select
            Pin(16, Pin.IN, Pin.PULL_UP),
            # Star power
            # Pin(27, Pin.IN, Pin.PULL_UP)
        ]

        # self.whammy = ADC(Pin(4))
        self.strum_pins = (
            Pin(5, Pin.IN, Pin.PULL_UP),
            Pin(14, Pin.IN, Pin.PULL_UP)
        )
        self.strum_pos = 0

        self.led = PWM(Pin(15))
        self.buttonmap = [0, 0, 0, 0, 0, 0, 0]
        self.joystick.set_state_change_callback(self.joystick_state_callback)
        self.joystick.start()
        pass

    def poll_buttons(self):
        self.strum_pos = ((not self.strum_pins[0].value()) - (not self.strum_pins[1].value()))*127
        # self.whammy_pos = self.whammy.read_u16()*(127/65535)

        self.buttonmap = [
            int(not self.buttons[0].value()),
            int(not self.buttons[1].value()),
            int(not self.buttons[2].value()),
            int(not self.buttons[3].value()),
            int(not self.buttons[4].value()),
            int(not self.buttons[5].value()),
            int(not self.buttons[6].value())
            # int(not self.buttons[7].value())
        ]
        self.notify_buttonmap()

    def notify_buttonmap(self):
        self.joystick.set_buttons(
            b1=self.buttonmap[0],
            b2=self.buttonmap[1],
            b3=self.buttonmap[2],
            b4=self.buttonmap[3],
            b5=self.buttonmap[4],
            b6=self.buttonmap[5],
            b7=self.buttonmap[6]
            # b8=self.buttonmap[7]
        )

        self.joystick.set_axes(0, self.strum_pos) # self.whammy_pos, self.strum_pos)
        try:
            self.joystick.notify_hid_report()
        except:
            pass

    def advertise(self):
        self.joystick.start_advertising()
        
    def stop_advertise(self):
        self.joystick.stop_advertising()

    def joystick_state_callback(self):
        if self.joystick.get_state() is Joystick.DEVICE_IDLE:
            return
        elif self.joystick.get_state() is Joystick.DEVICE_ADVERTISING:
            return
        elif self.joystick.get_state() is Joystick.DEVICE_CONNECTED:
            gc.collect()
            return
        else:
            return

    def start(self):
        self.advertise()
        while True:
            if self.joystick.get_state() is Joystick.DEVICE_IDLE:
                self.joystick.start_advertising()
            self.poll_buttons()

if __name__ == "__main__":
    d = Device()
    d.start()
