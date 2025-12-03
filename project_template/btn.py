# Button handler implementation

import machine
import utime

class Button:
    def __init__(self, action: callable = lambda: None, pin: int = 18):

        self.pin = machine.Pin(pin, machine.Pin.IN, machine.Pin.PULL_UP)

        # Store pointer to function
        self.action = action

        # Configure an IRQ that will run a function when the button is pressed
        self.pin.irq(trigger=machine.Pin.IRQ_FALLING, handler=self.click)
        # Store current time - will be used for debouncing
        self.last_press = utime.ticks_ms()

    def click(self):
        # Handle debouncing
        # if current_time - last_press < 100ms, ignore the press
        current_time = utime.ticks_ms()
        if utime.ticks_diff(current_time, self.last_press) < 100:
            return
        
        # Note that in MicroPython we have to use utime.ticks_diff - we can't just
        # simply do something like last_time - time.time(). 

        self.last_press = current_time

        # Actually call the action.
        self.action()
