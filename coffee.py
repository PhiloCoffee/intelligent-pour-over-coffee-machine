# gear motor
# servo motor

# 测试各个档位
from hardware.motor import GearMotor, ServoMotor
from hardware.pump  import PumpControl
from util import logger
from time import sleep
import sys

import warnings
from gpiozero.exc import PWMSoftwareFallback

# Suppress specific warning
warnings.filterwarnings("ignore", category=PWMSoftwareFallback)

# def safe_sleep(tm, display, stop, intv = 1):
#     while (tm > 0):
#         if (stop.is_pressed):
#             display.display_text(["Machine stopped.","STOP is pressed.","","Bye, welcome to drink Next time !!"])
#             sys.exit()
#         if tm >= intv:
#             tm -= intv
#             sleep(intv)
#         else:
#             sleep(tm)
#             tm = 0

SM_PIN   = 18
GM_PIN_F = 19
GM_PIN_B = 20
PP_PIN   = 13
class Coffee:
    
    def __init__(self, ws = None, wstare = None, display = None, stop = None, mass_bean = None, mass_water= None, mode_list = None, mode = None, timer = None, K = None, next = None):
        self.gear_motor = GearMotor(GM_PIN_F,GM_PIN_B)
        self.servo_motor = ServoMotor(SM_PIN)
        self.pump = PumpControl(PP_PIN)
        self.ws = ws
        self.wstare = wstare
        self.display = display
        self.stop = stop
        self.mass_bean = mass_bean
        self.mass_water = mass_water
        self.mode_list = mode_list
        self.mode = mode
        self.Timer = timer
        self.K = K
        self.next = next
        #self.display = None
        #self.stop = None
    
    def safe_sleep(self, tm, display, stop, intv = 1):
        while (tm > 0):
            if (stop.is_pressed):
                display.display_text(["Machine stopped.","STOP is pressed.","","Bye, welcome to drink Next time !!"])
                sys.exit()
            if self.weight_water():
                return 1
            if tm >= intv:
                tm -= intv
                sleep(intv)
            else:
                sleep(tm)
                tm = 0
        return 0
    
    def weight_water(self):
        self.mass_water = self.ws.weight(5)
        self.mass_water = max(0, self.mass_water)
        self.display.display_text([f"Brewing {self.mode_list[self.mode]} coffee", "Pumping water...", f" Time: {int(self.Timer.elapsed())}",  f"Mass of water: {int(self.mass_water)}g"]) # [State: PUMP]
        #self.weight_display.display_text([f"Mass of Bean: {self.mass_bean}g", f"Mass of water: {self.mass_water}g"])
        if (self.mass_water >= self.K * self.mass_bean) or (self.next.is_pressed):
            return 1
        return 0
    
    """
        execute the coffee brewing given a brewing style.
    """
    def light_roast(self, display, stop, ws, wstare):
        self.display = display
        self.stop = stop
        # self.servo_motor.calibrate()
        self.servo_motor.move_to_angle(0)
        self.gear_motor.set_speed(90)
        self.gear_motor.go()
        self.pump.go()
        if self.weight_water():
            return 1
        if self.safe_sleep(5, self.display, self.stop):
            return 1
        self.pump.stop()

        self.servo_motor.move_to_angle(30)
        self.pump.go()
        if self.weight_water():
            return 1
        if self.safe_sleep(5, self.display, self.stop):
            return 1
        self.pump.stop()

        if self.safe_sleep(20, self.display, self.stop):
            return 1
        self.servo_motor.move_to_angle(0)
        self.pump.go()
        if self.weight_water():
            return 1
        if self.safe_sleep(5, self.display, self.stop):
            return 1
        self.pump.stop()

        self.servo_motor.move_to_angle(30)
        self.pump.go()
        if self.safe_sleep(3, self.display, self.stop):
            return 1
        self.servo_motor.move_to_angle(0)
        if self.safe_sleep(3, self.display, self.stop):
            return 1
        if self.weight_water():
            return 1
        if self.safe_sleep(5, self.display, self.stop):
            return 1
        self.pump.stop()

        self.gear_motor.stop()

        return 0
        

    def dark_roast(self, display, stop):
        self.display = display
        self.stop = stop
        # self.servo_motor.calibrate()
        self.servo_motor.move_to_angle(0)
        self.gear_motor.set_speed(90)
        self.gear_motor.go()
        self.pump.go()
        if self.weight_water():
            return 1
        if self.safe_sleep(5, self.display, self.stop):
            return 1
        self.pump.stop()

        self.servo_motor.move_to_angle(30)
        self.pump.go()
        if self.weight_water():
            return 1
        if self.safe_sleep(5, self.display, self.stop):
            return 1
        self.pump.stop()

        if self.safe_sleep(20, self.display, self.stop):
            return 1
        self.servo_motor.move_to_angle(0)
        self.pump.go()
        if self.weight_water():
            return 1
        if self.safe_sleep(5, self.display, self.stop):
            return 1
        self.pump.stop()

        self.servo_motor.move_to_angle(30)
        self.pump.go()
        if self.weight_water():
            return 1
        if self.safe_sleep(5, self.display, self.stop):
            return 1
        self.pump.stop()

        self.gear_motor.stop()

        return 0


    def hot_water(self):
        self.servo_motor.move_to_angle(30)
        sleep(2)
        
        self.pump.go()
        sleep(15)
        self.pump.stop()
        self.servo_motor.stop()



    def hot_rinse(self):
        print("Start hot rinse")
        self.servo_motor.move_to_angle(0)
        sleep(2)
        self.pump.go()

        self.gear_motor.set_speed(-100)
        self.gear_motor.go()
        sleep(5)

        self.gear_motor.set_speed(100)
        self.gear_motor.go()
        sleep(5)

        self.servo_motor.stop()
        self.pump.stop()
        self.gear_motor.stop()


if __name__ == "__main__":
    logger.setup_logger("Test coffee")
    test_coffee = Coffee()
    # test_coffee.light_roast()
    # test_coffee.light_roast()
    # test_coffee.hot_water()

    test_coffee.hot_rinse()