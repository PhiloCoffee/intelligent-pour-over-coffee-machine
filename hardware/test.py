import pump
import motor
from time import sleep
SM_PIN = 18
GM_PIN_F = 19
GM_PIN_B = 20


if __name__ == "__main__":
    pump = pump.PumpControl(pump_pin=13)
    pump.pump_for_duration(duration = 10)

    gear_motor = motor.GearMotor(GM_PIN_F,GM_PIN_B)
    
    # # Set speed to 50% forward
    gear_motor.set_speed(50)
    gear_motor.go()
    sleep(20)
    gear_motor.stop()
    # Set speed to 75% reverse
    gear_motor.set_speed(-75)
    gear_motor.go()
    sleep(20)
    