# CS 401 - Final Project Assignment

This is a **group** submission - you will work in small groups on this project.

In this final project, you will design a very simple IoT device that allows controlling the LED on the Pi Pico board from a web page.

You will use the Raspberry Pi Pico to complete this task. For controlling the LED you can refer to the first assignment in this course, which explains how to use the GPIO interface to turn the LED on and off. The example code in [Assignment 1](I_ASSIGN1.md) should be all you need to get started. 

## Requirements

Your project **must** incorporate the following functionality:

* A simple, hand-coded HTTP server to serve the web pages. (See the Tips section for hints on doing this!) You don't need to do *extensive* error handling - just basic checks for validity are acceptable.
* The web server should be able to share at least two pages - the main UI and a configuration page. The main page must provide a means of controlling the onboard LED. The configuration page must allow you to specify an SSID and password.
  * You do NOT need to implement Wi-Fi scanning functionality to select a broadcasting hotspot. You need only ask the user to type in their network SSID in one field and password in another.
* The web server should accept the SSID and password given by the user in configuration as an HTTP POST request to a given endpoint. Upon receiving SSID and password, the device should store those values in a config file (e.g. `config.json`), return a success message to the user, and then *reboot* the Pi Pico.
    > ![TIP]
    > To reboot the Pico, import the `machine` library and run `machine.reset()`
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
