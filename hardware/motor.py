#!/usr/bin/python3
# File: hardware/motor.py
# Control the motors with CLI for easy testing
import gpiozero as gz
import json
import os
from time import sleep

SM_PIN = 18
GM_PIN_F = 19
GM_PIN_B = 20

# Control for 370 gear motor 
class GearMotor:
    def __init__(self,forward_pin,backward_pin):
        # Initialize PWM device at the pin with an initial value of 0 (off)
        self.motor = gz.Motor(forward=forward_pin,backward=backward_pin)
        print("init gear...")
        sleep(0.1)

    def set_speed(self, new_speed):
        """ Set motor speed as a percentage of full speed. """
        self.motor.value = float(new_speed / 100  )
        print(f"Set speed for gear motor as {new_speed}%")
        sleep(0.1)

    def go(self):
        """ Set motor speed as a percentage of full speed. 
        Can be negative to indicate reverse direction. """
        print("Go gear")
        print(f"self.motor.value is {self.motor.value}")
        if self.motor.value < 0:
            self.motor.backward(-self.motor.value)
        else:
            self.motor.forward(self.motor.value) # Convert percentage to a 0-1 scale
        sleep(0.1)
        

    def stop(self):
        """ Stop the motor. """
        self.motor.stop()
        print("stop gear...")
        sleep(0.1)



class ServoMotor:
    def __init__(self, pin,calibration_button_pin = 1):
        self.servo = gz.Servo(pin)
        #self.calibration_button = gz.Button(calibration_button_pin)  # 触发校准的按钮

        # 这里的servo_values应根据实际测量调整
        self.angle_to_value = {
            0:  -0.5,       # 对应 0 度
            15: 0,   # 对应 15 度
            30: 0.5    # 对应 30 度
        }
        print("init servo...")
        sleep(0.1)
    
    def move_to_angle(self, angle):
        if angle in self.angle_to_value.keys():
            self.servo.value = self.angle_to_value[angle]
            print(f"Moved to {angle} degrees")
            sleep(0.3)
            self.servo.detach()

        else:
            print("Invalid angle specified")
        
    def stop(self):
        self.servo.detach()
        print("Stop servo...")
        sleep(0.1)


    def calibrate(self):
        print("Starting calibration...")
        # 移动到一个极限，假设最小值
        while not self.calibration_button.is_pressed:
            self.servo.value = 0 # TODO 
            sleep(0.05)  # 给予一定时间让servo响应
        self.servo.value = None  # 断电servo避免过载
        print("Calibration completed. Servo set to 0 degrees.")

    def adjust_servo(self):
        # 用于微调servo_value与实际角度的对应关系
        for angle, value in self.angle_to_value.items():
            self.servo.value = value
            print(f"Adjusting to {angle} degrees. Current value: {value}")
            # Assume adjustment input from user or measurements
            new_value = float(input(f"Enter new servo value for {angle} degrees: "))
            self.angle_to_value[angle] = new_value
            print("New value set.")

def servo_test(gpio_pwm_id):
    servo = gz.Servo(int(gpio_pwm_id))
    servo_data = []  # 使用列表存储每次的控制值变化和角度变化

    print("Servo Control Initialized. Enter value change (e.g., +0.5 or -0.3) followed by the actual angle change.")
    print("Type 'save' to save data and 'exit' to quit.")
    
    current_value = 0  # 记录当前的servo value

    while True:
        command = input("Enter value change or command: ")
        if command.lower() == 'save':
            save_data(servo_data)
            print("Data saved to './servo_dict.json'.")
        elif command.lower() == 'exit':
            print("Exiting program.")
            break
        else:
            try:
                value_change = float(command)
                current_value += value_change
                if -1 <= current_value <= 1:
                    servo.value = current_value
                    print(f"Servo set to new position: {current_value}")
                    angle_change = input("Please enter the corresponding angle change: ")
                    servo_data.append({'value_change': value_change, 'angle_change': angle_change})
                else:
                    print("Invalid cumulative value: Out of bounds [-1, 1]. Adjusting back.")
                    current_value -= value_change  # Reset to previous value
            except ValueError:
                print("Invalid input: Please enter a value change (e.g., +0.5, -0.3), 'save', or 'exit'.")

def save_data(data):
    if not os.path.exists('./'):
        os.mkdir('./')
    with open("./servo_dict.json", "w") as f:
        json.dump(data, f, indent=4)



# 使用方法
if __name__ == "__main__":
    # servo_test(SM_PIN)
    
    servo_controller = ServoMotor(SM_PIN)
    # while(True):
    #     servo_controller.move_to_angle(0)
    #     sleep(1)
    #     servo_controller.move_to_angle(15)
    #     sleep(1)
    #     servo_controller.move_to_angle(30)
    #     sleep(1)
    #     servo_controller.move_to_angle(15)
    #     sleep(1)
    #     servo_controller.stop()


    # servo_controller.adjust_servo()
    servo_controller.move_to_angle(0)
    sleep(0.5)
    servo_controller.move_to_angle(15)
    sleep(0.5)
    servo_controller.move_to_angle(30)
    sleep(0.5)
    servo_controller.stop()


    # servo_test(18)
    
    # Initialize motor with GPIO pins (replace with actual GPIO numbers)
    gear_motor = GearMotor(GM_PIN_F,GM_PIN_B)
    
    # # Set speed to 50% forward
    gear_motor.set_speed(50)
    gear_motor.go()
    sleep(20)
    gear_motor.stop()
    # Set speed to 75% reverse
    gear_motor.set_speed(-75)
    gear_motor.go()
    sleep(20)
    
    # # Stop the motor
    # gear_motor.stop()