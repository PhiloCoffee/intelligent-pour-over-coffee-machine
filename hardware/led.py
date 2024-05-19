# File: hardware/led.py
# Control for small LED bulbs
from gpiozero import LED, Button
from time import sleep, localtime, strftime

# digital display LED. 4 * 8 = 32 LEDs
# Reference: http://blog.mangolovecarrot.net/2015/05/05/raspi-study05
# modified to gpiozero version
class LEDDisplay:
    def __init__(self):
        # Define LEDs
        # e,d,dp,c,g,3,b,2,1,f,a,0
        # 5,6,10,27,9,21,22,20,16,11,13,23
        self.leds = {
            'A': LED(13),
            'B': LED(22),
            'C': LED(27),
            'D': LED(6),
            'E': LED(5),
            'F': LED(11),
            'G': LED(9),
            'DP': LED(10)
        }
        # Define digit select pins
        self.digits = [LED(23), LED(16), LED(20), LED(21)]

        # Define the button
        #self.button = Button(27, pull_up=True)
        #self.button = Button(27)

    def show_digit(self, digit_no, num, show_dot_point):
        # Turn off all digits
        for digit in self.digits:
            digit.off()

        # Segment states for numbers 0-9
        segment_states = [
            {'A': False, 'B': False, 'C': False, 'D': False, 'E': False, 'F': False, 'G': True,  'DP': not show_dot_point}, # 0
            {'A': True,  'B': False, 'C': False, 'D': True,  'E': True,  'F': True,  'G': True,  'DP': not show_dot_point}, # 1
            {'A': False, 'B': False, 'C': True,  'D': False, 'E': False, 'F': True,  'G': False, 'DP': not show_dot_point}, # 2
            {'A': False, 'B': False, 'C': False, 'D': False, 'E': True,  'F': True,  'G': False, 'DP': not show_dot_point}, # 3
            {'A': True,  'B': False, 'C': False, 'D': True,  'E': True,  'F': False, 'G': False, 'DP': not show_dot_point}, # 4
            {'A': False, 'B': True,  'C': False, 'D': False, 'E': True,  'F': False, 'G': False, 'DP': not show_dot_point}, # 5
            {'A': False, 'B': True,  'C': False, 'D': False, 'E': False, 'F': False, 'G': False, 'DP': not show_dot_point}, # 6
            {'A': False, 'B': False, 'C': False, 'D': True,  'E': True,  'F': True,  'G': True,  'DP': not show_dot_point}, # 7
            {'A': False, 'B': False, 'C': False, 'D': False, 'E': False, 'F': False, 'G': False, 'DP': not show_dot_point}, # 8
            {'A': False, 'B': False, 'C': False, 'D': False, 'E': True,  'F': False, 'G': False, 'DP': not show_dot_point},  # 9
            {'A': True, 'B': True, 'C': True, 'D': True, 'E': True,  'F': True, 'G': False, 'DP': not show_dot_point}  # -
        ]

        # Set segment states
        for segment, state in segment_states[num].items():
            self.leds[segment].value = state

        # Activate the correct digit
        self.digits[digit_no].on()

    def display_time(self):
        hour = 0
        minute = 0
        while True:
            hour = int(strftime("%H", localtime()))
            minute = int(strftime("%M", localtime()))
            # Break the time/date into digits and display
            # LED 3 2 1 0
            self.show_digit(3, hour // 10, False)
            sleep(0.005)
            self.show_digit(2, hour % 10, True)
            sleep(0.005)
            self.show_digit(1, minute // 10, False)
            sleep(0.005)
            self.show_digit(0, minute % 10, False)
            sleep(0.005)
    
    def display_weight(self, weight):
        # Break the time/date into digits and display
        neg = 0
        if weight < 0:
            weight = 0 # will delete, for debug
            # neg = 1
        weight_int = int(weight)
        weight_dec = int((weight - weight_int) * 10)
        cnt = 0
        #print(weight_int)
        while cnt < 100:
            # LED 3 2 1 0
            self.show_digit(0, (weight_int // 100) % 10, False)
            sleep(0.002)
            self.show_digit(1, (weight_int // 10) % 10, False)
            sleep(0.002)
            self.show_digit(2, weight_int % 10, True)
            sleep(0.002)
            self.show_digit(3, weight_dec % 10, False)
            sleep(0.001)
            cnt += 1

if __name__ == "__main__":
    led4digit = LEDDisplay()
    while True:
        led4digit.display_weight(156.8)