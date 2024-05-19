from gpiozero import DigitalInputDevice, DigitalOutputDevice
import time
from gpiozero import Button
from time import sleep
'''
hx711_pi5.py
Author: @UnderD 

'''

def create_bool_list(size=8):

    return [False, False, False, False, False, False, False, False] # avoid mutable issues.

class HX711:
    def __init__(self, dout, pd_sck, gain=128):
        self.PD_SCK = DigitalOutputDevice(pd_sck)
        self.DOUT = DigitalInputDevice(dout)
        
        self.GAIN = 0
        self.OFFSET = 0
        self.SCALE = 1
        self.lastVal = 0

        self.set_gain(gain)

    def is_ready(self):
        return not self.DOUT.value

    def set_gain(self, gain):
        gain_map = {128: 1, 64: 3, 32: 2}
        self.GAIN = gain_map.get(gain, 1)
        self.PD_SCK.off()
        self.read()

    def read(self):
        while not self.is_ready():
            pass


        data_bits = [create_bool_list(), create_bool_list(), create_bool_list()]

        for j in range(2, -1, -1):
            for i in range(7, -1, -1):
                self.PD_SCK.on()
                data_bits[j][i] = self.DOUT.value
                self.PD_SCK.off()

        if all(item == True for item in data_bits[0]):
            if self.lastVal > 8388607:
                self.lastVal -= 16777216
            return self.lastVal
        
        #print(data_bits)
        
        bits = []
        for byte in reversed(data_bits):
            bits += byte

        #print(bits)
        self.lastVal = int(''.join(map(str, bits)), 2)
        if self.lastVal > 2**23-1:
            self.lastVal -= 2**24
        #print(self.lastVal)
        return self.lastVal

    def read_average(self, times=3):
        a = 0
        for _ in range(times):
            b = self.read()
            #print(b)
            a += b
        #a = sum(self.read() for _ in range(times)) / times
        a = a / times
        #print(a)
        return a

    def get_value(self, times=3):
        #print("OFFSET = ",self.OFFSET)
        return self.read_average(times) - self.OFFSET

    def get_units(self, times=3):
        return self.get_value(times) / self.SCALE

    def tare(self, times=15):
        self.set_offset(self.read_average(times))

    def set_scale(self, scale):
        self.SCALE = scale

    def set_offset(self, offset):
        self.OFFSET = offset

    def power_down(self):
        self.PD_SCK.off()
        self.PD_SCK.on()

    def power_up(self):
        self.PD_SCK.off()

# Example usage
if __name__ == "__main__":
    from led import LEDDisplay
    hx = HX711(14, 15) # check if gpio pins are used out or not
    hx.set_scale(28200)
    hx.tare()
    hx_button = Button(17)
    
    LED = LEDDisplay()

    try:
        #if hx_button.is_pressed:
        #    print("tare")
        #    hx.tare()
        while True:
            val = hx.get_units(3)
            #print(val)
            LED.display_weight(val)
            if val > 3000:
                print("OH NO")
            #sleep(0.5)
    except (KeyboardInterrupt, SystemExit):
        pass
