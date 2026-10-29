import adi
import numpy as np
import matplotlib.pyplot as plt
import time
import atexit

AD74413R_DAC_MAX_CODE = 8192

dev_uri = "ip:192.168.97.40"

"""
	Possible values:
	- max14906 selected as device: input, output, high_z
	- ad74413r selected as device: high_z, voltage_out, current_out,
				       voltage_in, current_in_ext, current_in_loop,
				       resistance, digital_input, digital_input_loop,
				       current_in_ext_hart, current_in_loop_hart

"""
channel_config = ["voltage_out", "voltage_out", "voltage_out", "resistance"]

# Possible values: 0, 1
channel_enable = [1, 1, 1, 1]

# Possible values: "ad74413r", "max14906"
channel_device = ["ad74413r", "ad74413r", "ad74413r", "ad74413r"]

swiot = adi.swiot(uri=dev_uri)
swiot.mode = "config"
swiot = adi.swiot(uri=dev_uri)

swiot.ch0_device = channel_device[0]
swiot.ch0_function = channel_config[0]
swiot.ch0_enable = channel_enable[0]
swiot.ch1_device = channel_device[1]
swiot.ch1_function = channel_config[1]
swiot.ch1_enable = channel_enable[1]
swiot.ch2_device = channel_device[2]
swiot.ch2_function = channel_config[2]
swiot.ch2_enable = channel_enable[2]
swiot.ch3_device = channel_device[3]
swiot.ch3_function = channel_config[3]
swiot.ch3_enable = channel_enable[3]
swiot.mode = "runtime"

ad74413r = adi.ad74413r(uri=dev_uri)
max14906 = adi.max14906(uri=dev_uri)
adt75 = adi.lm75(uri=dev_uri)
swiot = adi.swiot(uri=dev_uri)
swiot.mode = "runtime"
# Rev ID should be 0x8
print("AD74413R rev ID:", ad74413r.reg_read(0x46))

# Channels which may be used to sample data from the AD74413R
print("AD74413R input (ADC) channels:", ad74413r._rx_channel_names)

# Channels which may be used to set DAC values
print("AD74413R output (DAC) channels:", ad74413r._tx_channel_names)

print("ADT75 temperature reading:", adt75() * 62.5)

# Set the sampling rate for the resistance channel to 4800 for faster update 
ad74413r.channel["resistance3"].sampling_frequency = 4800

voltage_dac_scale = ad74413r.channel["voltage0"].scale
voltage_dac_offset = ad74413r.channel["voltage0"].offset

# EXERCISE 2: The control panel knob

# Control panels in a factory are full of knobs. The operator turns one to
# set the speed of a conveyor belt, the temperature of an oven, and so on.
# Inside most of those knobs there's a potentiometer, which is just a
# resistor that changes its value when you turn it.
# The knob on our board is a potentiometer too. We'll read it and use it to
# control the status light from exercise 1.


# No need to change anything here

# Same as in exercise 1, the number we write to a color at full brightness
LED_ON_CODE = 8000

ON = 100
OFF = 0

def set_light(red, green, blue):
    # each color goes from 0 (off) to 100 (full brightness)
    # anything below 0 or above 100 gets cut off, so the DAC can't get a bad value
    red = max(0, min(100, red))
    green = max(0, min(100, green))
    blue = max(0, min(100, blue))

    # voltage0 = red, voltage1 = green, voltage2 = blue
    ad74413r.channel["voltage0"].raw = int(red / 100 * LED_ON_CODE)
    ad74413r.channel["voltage1"].raw = int(green / 100 * LED_ON_CODE)
    ad74413r.channel["voltage2"].raw = int(blue / 100 * LED_ON_CODE)

def read_knob():
    # gives back the resistance of the potentiometer in Ohms
    return ad74413r.channel["resistance3"].processed / 1000

# turn the light off when the script stops, like in exercise 1
atexit.register(set_light, OFF, OFF, OFF)


# Your code goes below
# This time everything runs inside a while True loop, so it keeps going
# until you press Ctrl+C (you'll see some red error text when you stop it,
# that's normal).
# Whatever you write inside the loop has to be indented like the lines
# that are already there.

# the biggest value the knob gives, you will change this in step 5
KNOB_MAX = 11000

while True:
    # Step 1: read the knob (done for you)
    # run the script and turn the knob slowly from one end to the other.
    # write down the smallest and the biggest number you see
    resistance = read_knob()
    print("Knob:", resistance, "Ohms")

    # Step 2: turn the resistance into percent
    # the machine doesn't care about Ohms, it wants to know how far the knob
    # is turned: 0% all the way left, 100% all the way right.
    # tip: percent = resistance / KNOB_MAX * 100
    # print it so you can check it goes from 0 to 100


    # Step 3: dim the red light with the knob
    # set_light now takes a number from 0 to 100 for each color, so
    # set_light(50, 0, 0) is red at half brightness. Use your percent


    # Step 4: tank level alarm
    # pretend the knob is a sensor that measures how full a tank is.
    # put a # in front of your step 3 line and make the light show:
    #   green below 70%, yellow from 70% to 90%, red above 90%
    #
    # you'll need an if. It works like this:
    #
    #   if percent < 70:
    #       print("level is ok")
    #   elif percent < 90:
    #       print("almost full")
    #   else:
    #       print("overflow!")


    # Step 5: calibration
    # is your percent really 0 and 100 at the two ends? if not, change
    # KNOB_MAX above the loop to the biggest number you wrote down in step 1.
    # In a factory every sensor gets calibrated like this before it's used

    # Bonus: color fade
    # comment out step 4 and try to make the light go slowly from green to
    # red as you turn the knob (hint: when red goes up, green goes down)

    time.sleep(0.1)
