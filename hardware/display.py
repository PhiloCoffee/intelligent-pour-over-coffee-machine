# File: hardware/display.py
# Control for OLED and LED displays
#from hardware.gpio_interface import *
# Copyright (c) 2014 Adafruit Industries
# Author: Tony DiCola
# Ref: https://github.com/adafruit/Adafruit_CircuitPython_SSD1306

# SPDX-FileCopyrightText: Melissa LeBlanc-Williams for Adafruit Industries
# SPDX-License-Identifier: MIT

# This example is for use on (Linux) computers that are using CPython with
# Adafruit Blinka to support CircuitPython libraries. CircuitPython does
# not support PIL/pillow (python imaging library)!
#
# Ported to Pillow by Melissa LeBlanc-Williams for Adafruit Industries from Code available at:
# https://learn.adafruit.com/adafruit-oled-displays-for-raspberry-pi/programming-your-display

# Imports the necessary libraries...

import board
import digitalio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306

# Import all board pins.
from board import SCL, SDA
import busio

# Import the SSD1306 module.
import adafruit_ssd1306


class Display:
    
    def __init__(self, addr = 0x3C):
        # on a Raspberry Pi with the 128x32 display you might use:
        # Very important... This lets py-gaugette 'know' what pins to use in order to reset the display
        self.i2c = board.I2C()  # uses board.SCL and board.SDA
        # Reference: https://github.com/adafruit/Adafruit_BusIO
        #self.i2c = busio.I2C(board.SCL, board.SDA)  # uses board.SCL and board.SDA

        # Create the SSD1306 OLED class.
        # The first two parameters are the pixel width and pixel height.
        # Change these to the right size for your display!
        
        #self.oled = adafruit_ssd1306.SSD1306_I2C(128, 64, self.i2c, addr=addr)
        self.oled = adafruit_ssd1306.SSD1306_I2C(128, 64, self.i2c)
        # use different memory locations.

        # Clear display.
        self.oled.fill(0)
        self.oled.show()
    
    def display_temp_time(self, temp, brewing_time):
        # Create blank image for drawing.
        self.image = Image.new("1", (self.oled.width, self.oled.height))
        self.draw = ImageDraw.Draw(self.image)

        # Load a font in 2 different sizes.
        # Draw the text
        self.draw.text((10, 0), f"Temp: {temp} °C", fill=255)
        self.draw.text((10, 10), f"Brewing time: {brewing_time} s", fill=255)

        # Display image
        self.oled.image(self.image)
        self.oled.show()
    
    """
        display_text: 
            Input: text - a string list for displaying each line.
        Function:
            Display the user interaction text. Maximum 20 characters per line.
            Display content:
                - ["COFFEE MACHINE", "ECE 445", "Capstone", "Select a style", "to brew.", "LIGHT/DARK/HOT"] # [State: RESET]
                - ["Selected cooking", mode, "Coffee", "Plz put beans", "and press START."] # [State: SET_OP]
                - ["No enough beans."] # [State: SET_OP]
                - ["Selected cooking", mode, "Coffee...", f"Time: {self.Timer.elapsed()}"] # [State: EXEC, T-CLR] # mode is a string (HOT/LIGHT/DARK)
                - ["Pumping water...", "", "", f"Time: {self.Timer.elapsed()}"] # [State: PUMP]
                - ["Heating water...", "", "", f"Time: {self.Timer.elapsed()}", f"Temp: {temp} °C"] # [State: HEAT]
                - ["Flowing water...", "", "", f"Time: {self.Timer.elapsed()}", f"Temp: {temp} °C"] # [State: FLOW]
                - [f"Brewing {mode}...", "", "", f"Time: {self.Timer.elapsed()}", f"Temp: {temp} °C"] # [State: EXE-H/L/R, BREAK] # mode is a string (HOT/LIGHT/DARK)
                - ["Finish Brewing!", "Enjoy the coffee!", "", f"Time: {self.Timer.elapsed()}"] # [State: FINISH]
    """
    def display_text(self, text):
        # Create blank image for drawing.
        self.image = Image.new("1", (self.oled.width, self.oled.height))
        self.draw = ImageDraw.Draw(self.image)

        # Load a font in 2 different sizes.
        # Draw the text
        for i in range(len(text)):
            self.draw.text((0, i * 10), text[i], fill=255)

        # Display image
        self.oled.image(self.image)
        self.oled.show()
        
    def display_points(self):
        # Create the I2C interface.
        self.i2c = busio.I2C(SCL, SDA)

        # Create the SSD1306 OLED class.
        # The first two parameters are the pixel width and pixel height.  Change these
        # to the right size for your display!
        display = adafruit_ssd1306.SSD1306_I2C(128, 32, self.i2c)
        # Clear the display.  Always call show after changing pixels to make the display
        # update visible!
        display.fill(0)

        display.show()

        # Set a pixel in the origin 0,0 position.
        display.pixel(0, 0, 1)
        # Set a pixel in the middle 64, 16 position.
        display.pixel(64, 16, 1)
        # Set a pixel in the opposite 127, 31 position.
        display.pixel(127, 31, 1)
        display.show()