# Assignment 1: Working with MicroPython

In this exercise you will first install MicroPython onto your Raspberry Pi Pico, and you will then write a simple Hello World program. Additionally, you'll explore memory usage constraints and their effects.

## Part 1: Install MicroPython

Download the MicroPython file from the OneDrive link given on D2L. Alternatively you can download it directly from [MicroPython's page on the Pi Pico W](https://micropython.org/download/RPI_PICO_W/). You need the `.uf2` file.

Connect the USB cable to the Pico, but **do not yet connect the other end to your computer!**

First, **press and hold down the small white button** on the Pico board. It is labeled `BOOTSEL`. **While holding down the button**, attach the USB cable to your PC. When you do this, the Pi Pico should appear on your computer as a drive.

Simply copy the `.uf2` file you downloaded on to the drive. Once it's finished, the drive will *automatically disconnect* from your computer. At this point, MicroPython is ready to run!

## Part 2: Installing a Dev Environment

You have two choices for development environments:

* VS Code, with the [MicroPico](https://marketplace.visualstudio.com/items?itemName=paulober.pico-w-go) extension
* The [Thonny IDE](https://thonny.org/), which provides native support for the Pi Pico running MicroPython.

Either IDE is acceptable, however note that *PyCharm is not well supported* for working with the Pi Pico.

## Part 3: Hello World!

Input the following code into your editor:

    import gc
    from machine import Pin
    import time

    print("Hello from Pi Pico W!")
    print("Available RAM:", gc.mem_free(), "bytes")

    # Print system info
    import sys
    print("MicroPython version:", sys.version)
    print("Platform:", sys.platform)

    # Print memory stats
    print("Free memory:", gc.mem_free())
    print("Allocated memory:", gc.mem_alloc())

    # For Pico W, the LED is accessed differently!
    led = Pin('LED', Pin.OUT)  # Note: 'LED' not 25 for Pico W

    print("Blinking LED 10 times...")
    for i in range(10):
        led.on()
        time.sleep(0.5)
        led.off()
        time.sleep(0.5)

    print("Program finished!")

Run the program! Copy the output into your submission document. If the LED is not blinking, double check your code.

## Part 4: Memory Management

As we've discussed, microcontrollers and embedded systems tend to have very limited memory. While this may feel limiting, it's also an opportunity to think about more efficient ways to utilize your computing resources!

Consider this program:

    import json
    import time
    import random

    print("Starting memory-intensive program...")
    print(f"Free memory at start: {gc.mem_free()} bytes")

    # Simulate sensor data collection
    sensor_data = []
    reading_id = 0

    try:
        # Imagine we are collecting 5,000 readings from a sensor.
        # Note: this code will crash on a Pi Pico!
        for i in range(5000):
            reading = {
                'id': reading_id,
                'timestamp': time.time(),
                'temperature': random.uniform(20.0, 30.0),
                'humidity': random.uniform(30.0, 70.0),
                'pressure': random.uniform(1000.0, 1020.0),
                'light_level': random.randint(0, 1024),
                'status': 'OK',
                'location': 'Lab Room 401',
                'sensor_model': 'DHT22-BMP280-LDR-Combo',
                'calibration_offset': 0.0,
                'raw_adc_values': [random.randint(0, 4095) for _ in range(10)]
            }
            sensor_data.append(reading)
            time.sleep(0.05) # simulate a delay when reading
            reading_id += 1
            
            # Print progress every 100 readings
            if i % 100 == 0:
                print(f"Collected {i} readings... Free memory: {gc.mem_free()}")
        
        # Now print the average of all of the "temperature" values.
        # (note: if we get here, we're probably not on a Pico...)
        avg = sum([i['temperature'] for i in sensor_data])

        print("The average temperature was:", avg)
        
    except MemoryError as e:
        print(f"Error: out of memory after {len(sensor_data)} readings")
        print(f"Current free memory: {gc.mem_free()} bytes")
        print("Exception:", e)

Write this program into your MicroPython environment and try to run it. Observe what happens. Take a screenshot or paste the output into your submission.

Finally, it's time to rework the problem into something that *can* run successfully on the Raspberry Pi Pico. Your task is to consider **how we can rework the program so that it successfully runs without crashing** while still being able to compute the average of 5,000 randomly generated sensor readings.

# Submission

Your submission must include:

* Evidence of your Hello World program working (screenshot of printed output is OK)
* Evidence of the crash in the unoptimized program given (screenshot showing exception handler)
* The code for your fixed version of the program that can run successfully

Submit your work to D2L no later than *Monday, November 3rd* at 11:59 PM.

## Grading

This assignment is worth **100 points**.

Components:

| Item | Points | Scoring |
|-|-|-|
| Evidence of Hello World | 15 | Full points if Hello World program shown working. Zero points if omitted. |
| Evidence of Unoptimized Program Crash | 15 | Full points if crash is shown. Zero points if not done. |
| Optimized Program | 70 | Full points if updated program runs successfully and still does all of the same work - it must compute 5,000 random records with all the given fields and compute the average temperature of all data records. It should then print that average temperature before exiting. Points are taken off for buggy code, incorrect logic, or code that is incomplete or can't be run. |
