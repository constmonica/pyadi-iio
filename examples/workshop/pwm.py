# Copyright (C) 2026 Analog Devices, Inc.
#
# SPDX short identifier: ADIBSD

"""Bit-bangs a PWM signal on a specified channel, in the background."""

import collections
import threading
import time

PWM_PERIOD = 0.05  # Time period for one cycle (s)
PWM_SAMPLE_HISTORY = 2000  # Max number of recorded on/off transitions to keep


class PwmThread(threading.Thread):

    def __init__(self, channel, period=PWM_PERIOD, duty_cycle=0):
        """
        This function initializes the PWM thread with a target channel,
        and, optionally, a period in seconds and duty cycle in percentage.

        :param channel: The IIO channel object whose "raw" attribute is
        toggled between 0 and 1 to bit-bang the PWM signal.
        :param period: The length of one PWM cycle, in seconds.
        :param duty_cycle: The initial duty cycle, as a percentage from 0
        (always low) to 100 (always high).
        """
        super().__init__(daemon=True)
        self._channel = channel
        self._period = period
        self._lock = threading.Lock()
        self._duty_cycle = max(0, min(100, duty_cycle))
        self._level = None
        self._stop_event = threading.Event()
        self._samples_lock = threading.Lock()
        self._samples = collections.deque(maxlen=PWM_SAMPLE_HISTORY)

    def get_samples(self):
        """
        This function returns a snapshot of the recorded on/off transitions.
        Used for plotting the digital channel voltage output over time

        :return: A list of (timestamp, level) tuples, where "timestamp" is
        a time.monotonic() value and "level" is 0 or 1.
        """
        with self._samples_lock:
            return list(self._samples)

    def get_waveform(self, start, end):
        """
        This function returns the PWM signal between two moments, ready to
        be plotted with drawstyle="steps-post".

        :param start: Beginning of the window, as a time.monotonic() value.
        :param end: End of the window, as a time.monotonic() value.
        :return: A (times, levels) tuple of lists. The first point is at
        "start" and the last one at "end", so the signal is drawn over the
        whole window even when it didn't change inside it.
        """
        times = [start]
        levels = [0]
        for timestamp, level in self.get_samples():
            if timestamp <= start:
                levels[0] = level
            elif timestamp <= end:
                times.append(timestamp)
                levels.append(level)
        times.append(end)
        levels.append(levels[-1])
        return times, levels

    @property
    def duty_cycle(self):
        """
        This property returns the current PWM duty cycle.

        :return: The duty cycle, as a percentage from 0 to 100.
        """
        with self._lock:
            return self._duty_cycle

    @duty_cycle.setter
    def duty_cycle(self, value):
        """
        This setter sets the PWM duty cycle, clamped to a valid range.

        :param value: The desired duty cycle, as a percentage. Values
        outside the 0-100 range are clamped to the nearest bound.
        """
        with self._lock:
            self._duty_cycle = max(0, min(100, value))

    def stop(self):
        """
        This function stops the PWM thread and leaves the channel low.
        It waits for the thread to exit first, so the thread can't drive
        the channel high again after it was turned off.
        """
        self._stop_event.set()
        if self.is_alive():
            self.join()
        self._channel.raw = 0

    def run(self):
        """
        This function is the PWM thread's main loop. It drives the channel
        high for the "on" portion of the period and low for the "off"
        portion, based on the current duty cycle, until stop() is called.
        The cycles are scheduled against the clock, so the time spent
        writing to the channel doesn't stretch the period.
        """
        cycle_start = time.monotonic()
        while not self._stop_event.is_set():
            on_time = self.duty_cycle / 100 * self._period

            if on_time > 0:
                self._write(1)
                on_end = cycle_start + on_time
                if self._stop_event.wait(max(0, on_end - time.monotonic())):
                    break
            if on_time < self._period:
                self._write(0)

            cycle_start += self._period
            now = time.monotonic()
            if cycle_start < now - self._period:
                # fell more than one period behind, start again from now
                cycle_start = now
            self._stop_event.wait(max(0, cycle_start - now))

    def _write(self, level):
        # only talk to the board when the level actually changes, so 0% and
        # 100% don't cause any writes at all
        if level != self._level:
            self._channel.raw = level
            self._level = level
            self._record_sample(level)

    def _record_sample(self, level):
        with self._samples_lock:
            self._samples.append((time.monotonic(), level))
