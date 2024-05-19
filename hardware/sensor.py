# File: hardware/led.py
# Control for differnt kind of sensors

import time
import sys
from hardware.hx711_pi5 import HX711

class WeightSensor:
    
    def __init__(self, SDA = 14, SCK = 15):
        self.dout_pin = SDA
        self.pd_sck_pin = SCK
        self.hx = HX711(dout=self.dout_pin, pd_sck=self.pd_sck_pin)
        #self.hx.set_reading_format("MSB", "MSB")
        #self.hx.set_reference_unit(1)  # 这里需要根据你的实际情况调整
        #self.hx.reset()
        self.hx.set_scale(28200)
        self.hx.tare()

    def cleanAndExit(self):
        print("Cleaning...")
        if self:
            self.power_down()
        print("Bye!")
        sys.exit()

    def weight(self, times = 5):
        return self.hx.get_units(times)


if __name__ == '__main__':
    # File: hardware/led.py
    # Control for differnt kind of sensors

    def cleanAndExit():
        print("Cleaning...")
        if hx:
            hx.power_down()
        print("Bye!")
        sys.exit()

    # 创建一个HX711对象
    hx = HX711(dout_pin=2, pd_sck_pin=3)
    hx.set_reading_format("MSB", "MSB")

    # 校准HX711
    hx.set_reference_unit(1)  # 这里需要根据你的实际情况调整
    hx.reset()
    hx.tare()

    print("Tare done! Add weight now...")

    # get the weight
    while True:
        val = hx.get_weight(5)
        print(f"Weight: {val} grams")

        hx.power_down()
        hx.power_up()
        time.sleep(0.5)