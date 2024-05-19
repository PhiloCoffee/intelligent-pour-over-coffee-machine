from gpiozero import OutputDevice, Button
from time import sleep

class PumpControl:
    def __init__(self, pump_pin=13 ):
        self.pump = OutputDevice(pump_pin)
        # self.control_button = Button(control_button_pin)  # This could be a manual override button

    def go(self):
        self.pump.on()
        sleep(0.1)
        print("Pump is ON")

    def stop(self):
        self.pump.off()
        sleep(0.1)
        print("Pump is OFF")

    def pump_for_duration(self, duration):
        """Turns the pump on for a specified duration in seconds."""
        self.go()
        sleep(duration)  # Pump will stay on for 'duration' seconds
        self.stop()
        sleep(0.1)
        print(f"Pump has been turned off after {duration} seconds")



# Usage example
if __name__ == "__main__":
    pump = PumpControl(pump_pin=13)
    pump.pump_for_duration(duration = 10)
