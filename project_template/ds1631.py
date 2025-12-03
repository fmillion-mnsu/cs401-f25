# Driver for DS1631 Digital Temperature Sensor on Pi Pico

import machine

class DS1631:
    def __init__(self, i2c: machine.I2C=None, address=0x48):
        self.i2c = i2c
        self.address = address

        if self.i2c is None:
            self.i2c = machine.I2C(0, scl=machine.Pin(17), sda=machine.Pin(16), freq=10000)
        
        self.start_conversion()

    def start_conversion(self):
        # Start temperature conversion
        self.i2c.writeto(self.address, bytearray([0x51]))

    def read_temperature(self):
        # Read temperature from the sensor
        self.i2c.writeto(self.address, bytearray([0xAA]))  # Command to read temperature
        temp_data = self.i2c.readfrom(self.address, 2)  # Read 2 bytes of temperature data
        temp_raw = (temp_data[0] << 8) | temp_data[1]
        
        # Convert raw data to Celsius
        if temp_raw & 0x8000:  # Negative temperature
            temp_raw = -((temp_raw ^ 0xFFFF) + 1)
        
        temperature_c = temp_raw / 256.0
        return temperature_c