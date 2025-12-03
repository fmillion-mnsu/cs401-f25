import btn
import ds1631
import led

# Your app's main code goes here

# This example prints the temperature then starts changing the LED color.
# It also prints every time you press the button.

import utime
l = led.LED()

ds = ds1631.DS1631()
print("Current temperature: " + str(ds.get_temp()) + "C")

def button_handler():
    print("You pressed the button")
btn = btn.Button(button_handler)

while True:
    for i in range(8):
        # Convert i into binary with three booleans
        b0 = bool(i & 0x1)
        b1 = bool(i & 0x2)
        b2 = bool(i & 0x4)
        # Set the LED color based on the booleans
        l.set_color(b0, b1, b2)
        # Pause 0.5seconds
        utime.sleep(0.5)

