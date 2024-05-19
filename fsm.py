from gpiozero import LED, Button
from util import Timer
from hardware.display import Display
from hardware.sensor import WeightSensor

from coffee import Coffee
import sys
from time import sleep, localtime, strftime

import warnings
from gpiozero.exc import PWMSoftwareFallback

# Suppress specific warning
warnings.filterwarnings("ignore", category=PWMSoftwareFallback)
class FSM:
    def __init__(self, logger):
        self.state = 0 # RESET state
        self.mode = 0
        # press this button can turn to SET_OP state
        #self.led_setop = LED(17)
        self.button_setop = Button(23)
        # press this button can start brewing light coffee
        #self.led_light = LED(16)
        self.button_light = Button(24)
        # press this button can start brewing dark coffee
        #self.led_dark = LED(15)
        self.button_dark = Button(25)
        
        self.logger = logger
        self.Timer = Timer()
        self.wait_time = 0.2
        
        self.mass_water = 0
        self.mass_bean = 40 # grams
        self.K = 15
        
        self.thre_pump_time_on = 3
        self.thre_pump_time_off = 5
        self.pump_timer = Timer()
        self.pump_switch = 0
        self.pump_start = 0
        
        # Weight Sensor
        self.ws = WeightSensor()
        self.wstare = Button(17)
        
        
        self.stop = Button(5)
        self.next = Button(9)
        self.is_next = 0
        
        self.display = Display(0x3C)
        #self.weight_display = Display(0x3D)
        self.mode_list = ['None','LIGHT','DARK']

        self.coffee = Coffee(self.ws, self.wstare, self.display, self.stop, self.mass_bean, self.mass_water, self.mode_list, self.mode, self.Timer, self.K, self.next)
    
    def fsm_test_button(self):
        # Test Each Button.
        if self.button_setop.is_pressed:
            self.logger.info("SETOP is pressed.")
        if self.button_light.is_pressed:
            self.logger.info("LIGHT is pressed.")
        if self.button_dark.is_pressed:
            self.logger.info("DARK is pressed.")
        if self.stop.is_pressed:
            self.logger.info("STOP is pressed.")
        if self.next.is_pressed:
            self.logger.info("NEXT is pressed.")
        if self.wstare.is_pressed:
            self.logger.info("TARE is pressed.")
    
    def check_danger(self):
        if self.stop.is_pressed:
            self.logger.info('STOP the Coffee Machine!!')
            # self.display.display_text(["Machine stopped.","","Bye!!"])
            self.display.display_text(["Machine stopped.","STOP is pressed.","===============","Bye,","Welcome Next time !!"])
            sys.exit()
    
    def reset(self):
        self.coffee.pump.stop()
        self.coffee.gear_motor.stop()
        self.coffee.servo_motor.stop()
        
    def button_func(self):
        
        # [State: RESET]
        dis_list = ["COFFEE MACHINE", "ECE 445/ME 470", "Capstone","May-15-2024","©PhiloCoffee Club","Press SETOP to Start"]
        
        self.display.display_text(dis_list)
        #dis_list.append("ABCDE")
        #self.weight_display.display_text(dis_list)
        while True:
            # [State: DAN]
            self.fsm_test_button()
            self.check_danger()
            
            # test SET_OP button
            if self.state == 0:
                if self.button_setop.is_pressed:
                    #self.logger.info('SET_OP button is pressed')
                    self.state = 1 # turn to SET_OP
                    self.logger.info('Setting the brewing style now')
                    self.display.display_text(["COFFEE MACHINE", "ECE 445", "Capstone", "Select a style", "to brew.", "LIGHT/DARK"])
                else:
                    pass
            
            if self.state == 1:
                # [State: SET_OP]
                # test LIGHT button
                if self.button_light.is_pressed and self.mode == 0:
                    self.logger.info('Start brewing LIGHT coffee')
                    self.mode = 1
                    mode = "LIGHT"
                    self.display.display_text(["Selected cooking", mode, "Coffee"])
                    sleep(2)
                    # start executing the brewing process
                    self.state = 3 # exec
                    self.exec()
                    # [State: FINISH]
                    self.display.display_text(["Finish Brewing!", f"Brewing {self.mode_list[self.mode]} coffee", "Enjoy the coffee!", f" Time: {int(self.Timer.elapsed())}s", "Press [SETOP] to", "brew another cup."])
                    # reset the mode again
                    self.mode = 0
                    self.state = 0
                    self.reset()
                
                # test DARK button
                if self.button_dark.is_pressed and self.mode == 0:
                    self.logger.info('Start brewing DARK coffee')
                    self.mode = 2
                    mode = "DARK"
                    self.display.display_text(["Selected brewing", mode, "Coffee"])
                    sleep(2)
                    # start executing the brewing process
                    self.state = 3 # exec
                    self.exec()
                    # [State: FINISH]
                    self.display.display_text(["Finish Brewing!", f"Brewing {self.mode_list[self.mode]} coffee", "Enjoy the coffee!", f" Time: {int(self.Timer.elapsed())}s", "Press [SETOP] to", "brew another cup."])
                    # reset the mode again
                    self.mode = 0
                    self.state = 0
                    self.reset()
            
            self.Timer.wait(self.wait_time)
            self.check_danger()
    
    def exec(self):
        # [State: EXEC] (Actually this state can be ignored.)
        #self.display.display_text(["Brewing", f"{self.mode_list[self.mode]} Coffee"])
        #self.display.display_text(["Beans & Hot Water", "Please!", "Press [Next]", "if continue"])
        while True:
            if self.wstare.is_pressed:
                self.logger.info('Taring the weight now.')
                self.ws.hx.tare()
            #self.mass_bean = self.ws.weight()
            #self.mass_bean = max(0, self.mass_bean)
            self.mass_bean = 15
            self.water_to_add = (int((self.K * self.mass_bean) / 250) + 1) * 250
            self.display.display_text([f"Brewing {self.mode_list[self.mode]} coffee", "Beans & water plz", "Press [Next] to brew",f"Mass of beans:{int(self.mass_bean)}g",f"{int(self.water_to_add)}mL water to add..."])
            #self.weight_display.display_text([f"Mass of beans:{self.mass_bean}g",f"{self.water_to_add}mL water to add..."])
            if self.next.is_pressed:
                self.is_next = 1
                break
            self.check_danger()
        # clear the timer.
        # print the timer onto the LCD display.
        sleep(0.5)
        # [State: T-CLR]
        # Here sets the coffee beans' weight.
        self.Timer.start() # time set to 0.
        self.coffee.Timer.start()
        #self.display.display_text(["Selected cooking", self.mode_list[self.mode], "Coffee...", f" Time: {int(self.Timer.elapsed())}s"])
        # get the mass of bean powder.
        #self.display.display_text(["Selected cooking", self.mode_list[self.mode], "Coffee...", f" Time: {int(self.Timer.elapsed())}s","Mass of Bean", f"{self.mass_bean}g"])

        #self.weight_display.display_text(["Mass of Bean", f"{self.mass_bean}g"])
        # whether to pump.
        self.state = 5
        self.pump_switch = 0 # turn off the pump.
        self.pump_timer.start()
        self.pump_start = 0
        while True:
            self.fsm_test_button()
            if not self.next.is_pressed:
                self.is_next = 0
            else:
                self.is_next = 1
            # Here tares the weight if WSTARE is pressed.
            if self.wstare.is_pressed:
                self.logger.info('Taring the weight now.')
                self.ws.hx.tare()
            
            # [State: DAN]
            self.check_danger()
            
            # [State: PUMP]
            if self.pump_switch == 1:
                # self.display.display_text(["Pumping water...", f"Time: {int(self.Timer.elapsed())}"]) # [State: PUMP]
                # the pumper is working now. {Add code here}
                pass
            
            # if (self.pump_start == 0):
            #     self.pump_start = 1
            #     self.pump_switch = 1 # start pumping.
            #     # turn on the PUMPING DEVICE.
            #     self.logger.info("Pumper starts pumping...")
            #     self.pump_timer.start()
            
            # if (self.pump_start == 1):
            #     if (self.pump_timer.elapsed() >= self.thre_pump_time_on) and (self.pump_switch == 0):
            #         self.pump_switch = 1 # start pumping.
            #         # turn on the PUMPING DEVICE.
            #         self.logger.info("Pumper starts pumping...")
            #         self.pump_timer.start()
                
            #     if (self.pump_timer.elapsed() >= self.thre_pump_time_off) and (self.pump_switch == 1):
            #         self.pump_switch = 0 # start pumping.
            #         self.logger.info("Pumper stops pumping...")
            #         # turn off the PUMPING DEVICE.
            #         self.pump_timer.start()
            
            # If the water temperature in the hot tank is reached to the threshold
            # start flowing.
            
            # control the motor! let it dance!
            if self.mode == 1:
                # we wanna LIGHT coffee!
                # [State: EXE-L]
                if self.coffee.light_roast(self.display, self.stop, self.ws, self.wstare):
                    break

            elif self.mode == 2:
                # we wanna DARK coffee!
                # [State: EXE-D]
                if self.coffee.dark_roast(self.display, self.stop, self.ws, self.wstare):
                    break
            # elif self.mode == 3:
            #     # we wanna Hot water!
            #     # [State: EXE After Capstone]
            #     self.coffee.hot_water(self.display, self.stop)

            # elif self.mode == 4:
            #     # we wanna rinse machine coffee!
            #     # [State: EXE After Capstone] 
            #     self.coffee.hot_rinse(self.display, self.stop)
            
            # [State: BREAK]
            # measure the mass of water.
            # if there is enough water, finish the execution.
            ## The weight sensor
            self.mass_water = self.ws.weight(5)
            self.mass_water = max(0, self.mass_water)
            self.display.display_text([f"Brewing {self.mode_list[self.mode]} coffee", "Pumping water...", f" Time: {int(self.Timer.elapsed())}",  f"Mass of water: {int(self.mass_water)}g"]) # [State: PUMP]
            #self.weight_display.display_text([f"Mass of Bean: {self.mass_bean}g", f"Mass of water: {self.mass_water}g"])
            if (self.mass_water >= self.K * self.mass_bean) or (self.next.is_pressed and self.is_next == 0):
                break
            
            # the coffee is brewed, enjoy it!
            self.check_danger()
        return
