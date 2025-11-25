# CS 401 - Final Project Assignment

This is a **group** submission - you will work in small groups on this project.

In this final project, you will design a very simple IoT device that allows reading a sensor and controlling a multicolor LED via a web interface.

You will use the Raspberry Pi Pico, along with the custom printed circuit board you have been given, to complete this task. The printed circuit board contains:

* A DS1631 temperature sensor (connected to the I2C-0 bus)
* An RGB LED, with its three signal lines connected to GPIO 16 (blue), 17 (green) and 18 (red)
* A pushbutton with its signal connected to GPIO 19

## Requirements

Your project **must** incorporate the following functionality:

* A simple, hand-coded HTTP server to serve the web pages. (See the Tips section for hints on doing this!) You don't need to do *extensive* error handling - just basic checks for validity are acceptable.
* The web server should be able to share at least two pages - the main UI and a configuration page. The main page must provide, at minimum, a readout of the temperature sensor and a means of controlling the RGB LED. The configuration page must allow you to specify an SSID and password.
  * You do NOT need to implement Wi-Fi scanning functionality to select a broadcasting hotspot. You need only ask the user to type in their network SSID in one field and password in another.
* The web server should accept the SSID and password given by the user in configuration as an HTTP POST request to a given endpoint. Upon receiving SSID and password, the device should store those values in a config file (e.g. `config.json`), return a success message to the user, and then *reboot* the Pi Pico.
    > ![TIP]
    > To reboot the Pico, import the `machine` library and run `machine.reset()`
* When the button on the device is pressed, **toggle** the state of the LED light - if it is off, turn it on and vice versa. *This should track with on/off operations done via the web UI* - if the light was turned On via the web UI, even if it was last turned off by button, pressing the button should again turn the light off.
* At startup (when your code begins running) the device should look for a config file. If a config file is found it should be read and the stored SSID and password should be acquired. In this case, the device should attempt to connect to the given hotspot for no less than 15 seconds. If, after 15 seconds, connection has not succeeded, the device should revert to configuration mode.
* In configuration mode it should NOT be possible to view the main interface - attempting to do so should redirect the user to the config page.

    For example, if your main app is at `/` and your config page is at `/config.html`, then when the device is in config mode, accessing `/` should return this response:

        HTTP/1.1 302 Moved
        Location: /config.html
        Content-Length: 0

    Remember that all HTTP responses MUST end with a blank line. If there is no payload, then this blank line should be the last thing in the response.

## Tips

### Development

During development, make sure you name your main program something other than `boot.py` or `main.py`. Both of these names are reserved and will automatically execute any time your Pi Pico starts up. During testing, it will be much easier for you if you don't actually enable the auto-run functionality - this means that every time you reboot your Pi Pico, you'll be able to directly access the Python terminal (and run other functions like uploading your code).

**Once you've fully tested everything,** you can rename your main application to `main.py`. If this file is present, MicroPython automatically runs it every time your Pico starts up.

> ![TIP]
> One of the first things your code should do is to check for an existing configuration for the Wi-Fi credentials! If one is found, the application should try to connect; you can detect whether this is successful by referring to [Checking connectivity](#checking-connectivity). Once both conditions are met - config exists and connection was successful - then you can move into your main workflow - i.e. controlling the device. 
> 
> If either condition fails, your code should revert to creating a hotspot with predefined information and offering the *configuration page*. This configuration page could be part of the main site, or it could be a separate "interface" - you have freedom and flexibility in how to best implement this!

### Checking connectivity

When you attempt to connect to a Wi-Fi hotspot in client mode (i.e. not creating your own access point on the Pico), the easiest way to detect whether the Wi-Fi connection suceeded is simply to check the value of `isconnected()` on your WLAN network object. You can do this in a loop with a timeout - if connection didn't occur within, say, 15 seconds, we assume a connection failure and resort to the config mode.

Here is a snippet of code that illustrates this:

```python
def connect(ssid, password) -> bool:
    """Connect to a Wi-Fi hotspot using SSID and password. Returns True if connected successfully; False otherwise."""

    # Configure network to run in station (client) mode
    sta = network.WLAN(network.STA_IF)
    sta.active(True)
    sta.connect(ssid, password)

    # Check connection status every second for 15s
    for _ in range(15):
        if sta.isconnected():
            print('Connected to', config['ssid'])
            print('IP address:', sta.ifconfig()[0])
            return True
        sleep(1)
    
    # No connection after 15s
    sta.disconnect()
    sta.active(False) # disable device so it can be later used for AP mode
    return False
```

### Working with I2C

The I2C bus is implemented in hardware on the Pico. This means you do *not* have to manage the actual signaling - you simply specify which pins your I2C device is connected to and use simple read/write operations to perform your functions.

On the custom circuit board, the I2C interface is connected to GPIO pins 0 and 1. 

To initialize an I2C interface, use this code:

    from machine import Pin, I2C

    i2c = I2C(0, scl=Pin(1), sda=Pin(0), freq=400_000)

Once you have an I2C interface, you can do the following:

* `i2c.scan()`: Scan for I2C devices. Returns a list of addresses at which an I2C device was detected.
* `i2c.writeto(addr, b'bytes')`: Write the bytes `bytes` to the I2C device at address `addr`. 
* `i2c.readfrom(addr, n)`: Read `n` bytes from `addr`.

Note that in I2C it's very common to first *write* a message and then immediately *receive* from the same device. For example, you might send a command that means "get current temperature", and you would then immediately read the correct number of bytes from the device that represents the temperature. (You will also need to do raw processing of those bytes in most cases!)

### LED Colors

The RGB LED on the custom circuit board can light in nearly any color imaginable. However, to save you the trouble of dealing with RGB values and conversion into PWM frequencies, you can simply work with the following table to create colors:

| Red | Green | Blue | Color |
|-----|-------|------|-------|
| Off | Off   | Off  | <span style="color:#555555">Black</span> |
| Off | Off   | On   | <span style="color:#0000ff">Blue</span> |
| Off | On    | Off  | <span style="color:#00ff00">Green</span> |
| Off | On    | On   | <span style="color:#00ffff">Cyan</span> |
| On  | Off   | Off  | <span style="color:#ff0000">Red</span> |
| On  | Off   | On   | <span style="color:#ff00ff">Magenta</span> |
| On  | On    | Off  | <span style="color:#ffff00">Yellow</span> |
| On  | On    | On   | <span style="color:#cccccc">White</span> |

You can induce these colors by simply turning GPIOs 16, 17 and 18 on or off, respectively. Note that setting all three GPIOs to off equals "black" - i.e. the light goes out.

### Running your code

When you are working with multiple files, you should use the "Upload project to Pico" option in the Action menu (Ctrl+Shift+P on Windows). This reuploads all files in your project to the Pico - including non-code files (like HTML files).

Once you've updated your code, you can open a local file in the project, and then right-click the file in the Explorer view and choose "Run current file on Pico". (Note that you need to open the file's code - this is a quirk of how the extension works.) This will cause that file to be immediately executed on your Pico, and any output will appear in a terminal window.

Alternatively (and more quickly), you can just `import` your file in the Python terminal to run it. There are two assumptions here:

* You've named your file with a filename compatible with a module (e.g. `iot.py` is fine (`import iot`), but `cs401-project-f25.py` would not be (you can't import `cs401-project-f25` because the minus signs are interpreted as operators).)
* Your file does NOT use the `if __name__ == "__main__"` pattern. On MicroPython it is advisable *not* to use this common pattern - which is OK since you are working in a constrained limited environment.

Note that `import`ing will *cache* your code. This means that you need to reboot the Pico to re-run your code if you've modified it - even if you break out of the application and re-upload the project (see below). If you try importing again, your code won't run, since Python sees it as "already imported".

### Updating your code

You should always update your code *locally*. While MicroPico does let you update code on-device, you still would need to reboot the device to reload the modules.

Your general workflow after making a change to your code locally should be:

1. *Reboot* the Pi Pico. This requires unplugging it and replugging it into your computer - the Pico W does not have a reset button.
2. In MicroPico, bring up the command palette and look for "Upload project to Pico" and choose it. 
3. Wait for the notification indicating the project has been uploaded. This will also overwrite/replace any files you already had on the Pico with the same names.
4. In your terminal (the Python REPL), type `import app`. (This assumes your main program is called `app.py` - if it's something else, `import` that instead. Note that you should not use any reserved characters - your filename should be all alphanumeric characters and underscores if you want to be able to import it this way.)
5. This will start your app. Since you're working with sockets, you'll likely need to restart anyway to kill the app.

### Handling HTTP

The HTTP protocol may feel complex but it is relatively straightforward and can be easily manipulated with basic string manipulation commands.

Here is the typical format of an HTTP request - this is an *example* of what a client will immediately send to your app after you've accepted the connection:

    GET / HTTP/1.1
    User-Agent: Mozilla/5.0 (compatible...)
    Accept: *
    <<blank line>>

Your response must look similar to this example:

    HTTP/1.1 200 OK
    Content-Length: 5
    Content-Type: text/plain

    Hello

#### HTTP Verbs

Each request will contain one *verb*. The `GET` verb, arguably the most common, is used to request something from the site. This is the verb used to retrieve a web page for display.

The only other verb you need to be aware of is `POST`, which you will use to accept the SSID and password from the user. 

You should *detect* other verbs but reply with an empty Method Not Allowed response if they are ever detected:

    HTTP/1.1 405 Method Not Allowed
    Content-Length: 0
    <<blank line>>

#### HTTP Response Codes

The main response codes you need to be aware of (and to send to the client) are:

* `200` - OK. Include the requested content in the response.
* `404` - File not found. The path given doesn't point to anything.
* `405` - Method not allowed. An unknown method was requested, or the path doesn't accept the given method (e.g. you can't `POST` to `/index.html`).
* `500` - Internal server error. Something went wrong on the server side.

### Odds and Ends

These are some random helpful tidbits that you might find useful in your programs.

**Check free memory**

```python
import gc

free_mem = gc.mem_free()
print("Free memory:", free_mem, "bytes")
```

**Check free space on filesystem**

```python
import os

statvfs = os.statvfs('/')
free_bytes = statvfs[0] * statvfs[3]
print("Free space:", free_bytes, "bytes")
```

**Create a hotspot (AP mode)**

```python
import network

ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid='MicroPython', password='Password1234')
```

**Connect to a hotspot (station mode)**

See the [Checking Connectivity](#checking-connectivity) section for a complete example.

**React when a button is pressed**

```python
from machine import Pin

def button_handler(pin):
    print("Button pressed!")
    # Put code here that you want to run when the button is pressed.

# Replace BUTTON_PIN with the GPIO number your button is connected to.
# For the CS 401 project, the button is connected to GPIO 19.
button = Pin(BUTTON_PIN, Pin.IN, Pin.PULL_UP)
button.irq(trigger=Pin.IRQ_FALLING, handler=button_handler)
```

**Debouncing**

*Debouncing* refers to the handling of repeated rapid triggers that can sometimes occur with button presses simply due to the physics of pressing the button. Miniscule variations in components can result in multiple triggers, milliseconds or even microseconds apart, occurring when the button is pressed. Debouncing involves tracking when the last button press occurred and ignoring successive presses that occur a very short time after the first press.

```python
last_press = 0 # initialize variable
def button_handler(pin):
    global last_press
    now = time.ticks_ms()
    if time.ticks_diff(now, last_press) > 200:  # 200 ms debounce
        last_press = now
        print("Button pressed!")
        # do stuff here
```
