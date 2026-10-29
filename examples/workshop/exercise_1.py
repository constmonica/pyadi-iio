import adi
import matplotlib.pyplot as plt
import numpy as np
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

channel_config = ["voltage_out", "voltage_out", "voltage_out", "voltage_out"]

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

# EXERCISE 1: Machine status light

# If you walk through a factory you'll see a light on top of most machines.
# The operator looks at it to know what's going on without walking up to
# the machine. Green means it's running fine, yellow is a warning, red means
# something went wrong and the machine stopped, and blue usually means the
# machine is waiting for someone to do something.
# The RGB LED on the board will be our machine's status light.


# No need to change anything here

# The DAC turns a number from 0 to 8191 into a voltage from 0 to 11 V.
# We write this number to a color to turn it on
LED_ON_CODE = 8000

ON = 1
OFF = 0

def set_light(red, green, blue):
    # voltage0 = red, voltage1 = green, voltage2 = blue
    ad74413r.channel["voltage0"].raw = int(red * LED_ON_CODE)
    ad74413r.channel["voltage1"].raw = int(green * LED_ON_CODE)
    ad74413r.channel["voltage2"].raw = int(blue * LED_ON_CODE)

# This turns the light off when the script stops (also when you press Ctrl+C).
# A real machine has to do this too, we call it going to a safe state
atexit.register(set_light, OFF, OFF, OFF)


# Your code goes below
# set_light(red, green, blue) - turn each color ON or OFF
# time.sleep(2) - wait 2 seconds

# Step 1: red light, the machine has a fault
# (we did this one for you so you can see how it works)
print("Machine state: FAULT")
set_light(ON, OFF, OFF)
time.sleep(2)

# Step 2: green light, the machine is running
# tip: copy the 3 lines from step 1 and change what you need


# Step 3: blue light, the machine is waiting for the operator


# Step 4: yellow light, warning
# careful, the LED has no yellow, you'll have to figure it out


# Step 5: start-up sequence
# now put a few of them in a row, like a machine would do when it starts:
# blue for 3 seconds, then green for 3, yellow for 2 and red for 2


# Bonus: flashing alarm
# When something is really wrong the red light usually flashes, so people
# notice it faster.
#
# You can repeat code with a for loop. Everything indented under the for
# line gets repeated. This one prints hello 3 times:
#
#   for i in range(3):
#       print("hello")
#
# Try to write your own loop that flashes the red light 5 times
# (half a second on, half a second off)

print("Done, the light turns off by itself now")
