# RGB LED driver module for Pi Pico

import machine

class LED:
    def __init__(self, pin_r: int = 18, pin_g: int = 17, pin_b: int = 16):
        self.red = machine.Pin(machine.Pin(pin_r), machine.Pin.OUT)
        self.green = machine.Pin(machine.Pin(pin_g), machine.Pin.OUT)
        self.blue = machine.Pin(machine.Pin(pin_b), machine.Pin.OUT)
        self.state = [True, True, True] # Default to full white

    def set_color(self, red: bool, green: bool, blue: bool):
        """Set the color of the RGB LED.
        
Arguments:
    red -- True to turn on red, False to turn off
    green -- True to turn on green, False to turn off
    blue -- True to turn on blue, False to turn off

Remarks:
    If you are not turning the light OFF - i.e. setting all three values to
    False - then the new state will be stored for later use. You can then
    use off() and on() to turn the light on and off to the same color."""
        
        self.red.on() if red else self.red.off()
        self.green.on() if green else self.green.off()
        self.blue.on() if blue else self.blue.off()

        # If we didn't just turn the light off, store the new state so we can use it later
        if not red and not green and not blue:
            self.state = [red, green, blue]

    def off(self):
        """Turn off the LED unconditionally."""
        self.set_color(False, False, False)

    def on(self):
        """Turn on the LED to the last stored state."""
        # Set color from the state
        self.set_color(*self.state)