import collections
import time
import adi
import numpy as np
import matplotlib.pyplot as plt

from pwm import PwmThread

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
channel_config = ["output", "voltage_in", "voltage_in", "high_z"]

# Possible values: 0, 1
channel_enable = [1, 1, 1, 1]

# Possible values: "ad74413r", "max14906"
channel_device = ["max14906","ad74413r", "ad74413r", "ad74413r"]

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

# EXERCISES: Playing with a finished PID controller

# This script is a complete fan controller. 
#This time you don't write code, you change the numbers below,
# run it and look at the plots. Stop it with Ctrl+C or by closing the plot
# window, the fan turns off by itself.
#
# Before every run, write down what you think will happen. Then run it and
# check if you were right. Change one thing at a time and put it back when
# you're done with a step.

# Step 1: read the PWM signal
# Run the script as it is and put your finger on the temperature sensor.
# The terminal prints the "PWM duty cycle". Look at the bottom plot: for how
# much of every cycle is the signal on? Does it match the number in the
# terminal? What does the plot look like when the duty cycle is 0% or 100%?

# Step 2: switching frequency
# Change PWM_FREQUENCY below to 1, then 5, 20 and 50. Listen to the fan and
# look at the fan speed and the PWM plot. At which frequency can you hear
# the fan speed up and slow down? At 50 Hz, do the short pulses still look
# right? Every on/off switch is a message over the network, so the board
# can't switch as fast as we want.

# Step 3: setpoint
# Look at the temperature the board has right now. Set setpoint below to 5
# degrees under it and run it, then 5 degrees above it. What does the fan
# do? Can the controller reach the setpoint? Why not?

# Step 4: tuning, one letter at a time
# Do the same test every time: finger on the sensor for 30 seconds, then
# let go and wait 30 seconds.
#  a) Only P: set Ki = 0 and Kd = 0, try Kp = 1.5, 10 and 30. Does the
#     temperature get back down to the setpoint?
#  b) Add I: keep your best Kp, try Ki = 0.2, 1 and 5. Is the difference
#     to the setpoint gone? Does it go past the setpoint now?
#  c) Add D: try Kd = 1, 20 and 50. Is there less overshoot? What does the
#     fan speed plot look like when Kd is big?


# Constants for PWM control
# Every on/off switch is a write over the network, so a few ms per edge is
# the limit. 20 Hz keeps low duty cycles accurate; raise it if the link is fast.
PWM_FREQUENCY = 20  # Frequency for fan control (Hz)
PWM_PERIOD = 1.0 / PWM_FREQUENCY  # Time period for one cycle (s)
DC_RPM = 4500  # Max number of RPM for the fan

# The PID loop runs at a fixed rate, independent of the PWM frequency, so the
# gains below mean the same thing on every iteration
CONTROL_PERIOD = 1.0  # Time between two PID updates (s)

# PID parameters for temperature control
Kp = 1.5
Ki = 1
Kd = 1
setpoint = 28.0  # Temperature setpoint in degrees Celsius

# Initialize PID control variables
integral = 0
previous_error = 0

# Plot settings
PLOT_WINDOW = 180  # Seconds of history shown on the temperature and fan plots
PWM_PLOT_CYCLES = 10  # Number of PWM cycles shown on the bottom plot

PLOT_POINTS = int(PLOT_WINDOW / CONTROL_PERIOD) + 1
time_data = collections.deque(maxlen=PLOT_POINTS)
temperature_data = collections.deque(maxlen=PLOT_POINTS)
pwm_data = collections.deque(maxlen=PLOT_POINTS)
fan_rpm = collections.deque(maxlen=PLOT_POINTS)

# --- Helper Functions ---

# PID control function
def pid_control(current_temperature):
    """
    This function implements a PID control algorithm to regulate a system based on
    a temperature input.

    :param current_temperature: The "current_temperature" parameter is the current temperature value
    that is used as input to the PID control algorithm. This parameter represents the actual temperature
    of the system that the PID controller is trying to control.
    """
    global integral, previous_error

    # Calculate error
    error = -(setpoint - current_temperature)

    # Proportional, Integral, and Derivative terms
    proportional = Kp * error
    integral += error * Ki
    # Keep the integral within the duty cycle range, otherwise it keeps
    # growing while the fan is saturated and the fan reacts late (windup)
    integral = np.clip(integral, 0, 100)
    derivative = Kd * (error - previous_error)
    previous_error = error

    # PID output for fan speed control
    pid_output = proportional + integral + derivative

    # Convert PID output to PWM duty cycle (0-100%)
    pwm_duty_cycle = np.clip(pid_output, 0, 100)
    print(f"Error: {error:.2f} | PID output: {pid_output:.2f} | "
          f"PWM duty cycle: {pwm_duty_cycle:.0f} %")

    return pwm_duty_cycle


class PlotBlitter:

    def __init__(self, fig, artists):
        """
        This function sets up blitting for a figure: the static parts (axes,
        labels, grid, legends) are rendered once and cached, and only the
        given artists are redrawn on every update.

        :param fig: The matplotlib figure to update.
        :param artists: The artists that change between updates. They are
        excluded from the cached background.
        """
        self._fig = fig
        self._canvas = fig.canvas
        self._artists = artists
        self._background = None
        # backends that can't blit fall back to redrawing the whole figure
        self._use_blit = self._canvas.supports_blit
        for artist in artists:
            artist.set_animated(self._use_blit)
        self._canvas.mpl_connect("draw_event", self._on_draw)

    def _on_draw(self, event):
        # every full draw (first show, resize, new axis limits) refreshes the
        # cached background
        self._background = self._canvas.copy_from_bbox(self._fig.bbox)
        self._draw_artists()

    def _draw_artists(self):
        for artist in self._artists:
            self._fig.draw_artist(artist)

    def update(self, full_redraw=False):
        """
        This function puts the current artist data on screen.

        :param full_redraw: Set when something outside the artists changed,
        like the axis limits, so the cached background has to be rebuilt.
        """
        if not self._use_blit:
            self._canvas.draw_idle()
        elif full_redraw or self._background is None:
            self._canvas.draw()
        else:
            self._canvas.restore_region(self._background)
            self._draw_artists()
            self._canvas.blit(self._fig.bbox)
        self._canvas.flush_events()


def create_plots():
    """
    This function creates the figure and the line objects once. Later
    updates only change the line data, see update_plots().
    """
    global fig, temp_ax, rpm_ax, temp_line, rpm_line, pwm_line, blitter

    fig, (temp_ax, rpm_ax, pwm_ax) = plt.subplots(
        3, 1, figsize=(8, 9), gridspec_kw={"height_ratios": [3, 3, 2]})
    # the temperature and fan plots share the time axis
    rpm_ax.sharex(temp_ax)

    # Plot Temperature vs. Time
    (temp_line,) = temp_ax.plot([], [], label="Actual Temperature")
    temp_ax.axhline(setpoint, color='r', linestyle='--', label="Setpoint")
    temp_ax.set_xlim(0, PLOT_WINDOW)
    temp_ax.set_ylim(setpoint - 2, setpoint + 2)
    temp_ax.set_ylabel("Temperature (°C)")
    temp_ax.legend(loc="upper left")
    temp_ax.grid(True)

    # Plot Fan Speed vs. Time
    (rpm_line,) = rpm_ax.plot([], [], label="Fan Speed", color="b")
    rpm_ax.set_ylim(-0.05 * DC_RPM, 1.05 * DC_RPM)
    rpm_ax.set_xlabel("Time (s)")
    rpm_ax.set_ylabel("Speed (RPM)")
    rpm_ax.legend(loc="upper left")
    rpm_ax.grid(True)

    # Plot PWM Signal, the last few cycles up to now
    (pwm_line,) = pwm_ax.plot([], [], label="PWM Signal", color='g',
                              drawstyle="steps-post")
    pwm_ax.set_xlim(-PWM_PLOT_CYCLES * PWM_PERIOD, 0)
    pwm_ax.set_ylim(-0.2, 1.2)
    pwm_ax.set_yticks([0, 1], ["off", "on"])
    pwm_ax.set_xlabel(f"Time relative to now (s), PWM at {PWM_FREQUENCY} Hz")
    pwm_ax.set_ylabel("PWM Signal")
    pwm_ax.legend(loc="upper left")
    pwm_ax.grid(True)

    fig.tight_layout()
    blitter = PlotBlitter(fig, [temp_line, rpm_line, pwm_line])
    plt.show(block=False)
    plt.pause(0.1)


def update_plots(pwm):
    """
    This function updates the line data and puts it on screen. The axis
    limits only change when the data leaves them, so most updates only
    redraw the three lines.

    :param pwm: The PwmThread whose output signal is shown on the bottom plot.
    """
    full_redraw = False

    # move the time axis forward by half a window when the data reaches its end
    xmin, xmax = temp_ax.get_xlim()
    if time_data[-1] > xmax:
        xmax = time_data[-1] + PLOT_WINDOW / 2
        temp_ax.set_xlim(xmax - PLOT_WINDOW, xmax)
        full_redraw = True

    # grow the temperature axis when the temperature goes outside of it
    ymin, ymax = temp_ax.get_ylim()
    if not ymin <= temperature_data[-1] <= ymax:
        temp_ax.set_ylim(min(ymin, temperature_data[-1] - 1),
                         max(ymax, temperature_data[-1] + 1))
        full_redraw = True

    temp_line.set_data(time_data, temperature_data)
    rpm_line.set_data(time_data, fan_rpm)

    pwm_end = time.monotonic()
    pwm_times, pwm_levels = pwm.get_waveform(
        pwm_end - PWM_PLOT_CYCLES * PWM_PERIOD, pwm_end)
    pwm_line.set_data(np.array(pwm_times) - pwm_end, pwm_levels)

    blitter.update(full_redraw)


def wait_until(deadline):
    """
    This function waits until the given moment while keeping the plot
    window responsive (moving, resizing, zooming).

    :param deadline: The moment to wait for, as a time.monotonic() value.
    """
    while plt.fignum_exists(fig.number):
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            break
        fig.canvas.start_event_loop(remaining)

# --- Main Execution Loop ---

# The PWM signal is generated in the background, so the control loop and the
# plots never block the switching and vice versa
fan_pwm = PwmThread(max14906.channel["voltage0"], PWM_PERIOD)

try:
    # Verify device channels
    print("MAX14906 output/input channels:", max14906._tx_channel_names, max14906._rx_channel_names)
    print("AD74413R input (ADC) channels:", ad74413r._rx_channel_names)
    print(f"Initial ADT75 temperature reading: {adt75() * 62.5} °C")

    create_plots()
    fan_pwm.start()

    start_time = time.monotonic()
    next_loop_time = start_time

    # Main loop for temperature control and fan speed adjustment, runs until
    # CTRL+C is pressed or the plot window is closed
    while plt.fignum_exists(fig.number):
        # Read the current temperature from ADT75 sensor
        current_temperature = adt75() * 62.5
        print(f"Current temperature: {current_temperature} °C")

        # Get the PID-adjusted PWM duty cycle based on the temperature
        pwm_output = pid_control(current_temperature)

        # Hand the new duty cycle to the PWM thread, it applies it on the
        # next cycle
        fan_pwm.duty_cycle = pwm_output
        fan_speed = DC_RPM * pwm_output / 100

        # Append data for plotting
        time_data.append(time.monotonic() - start_time)
        temperature_data.append(current_temperature)
        pwm_data.append(pwm_output)
        fan_rpm.append(fan_speed)

        update_plots(fan_pwm)

        # keep a steady loop rate; if an iteration ran late, start again from now
        next_loop_time = max(next_loop_time + CONTROL_PERIOD, time.monotonic())
        wait_until(next_loop_time)

except KeyboardInterrupt:
    pass

finally:
    # Stop the fan when CTRL+C is pressed or the window is closed
    fan_pwm.stop()
    print("PWM stopped and voltage set to 0.")
