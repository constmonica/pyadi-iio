# SDR_functions.py
# These are Pluto control functions

import pickle
import sys
import time

import adi
import numpy as np
from numpy import (
    absolute,
    argmax,
    argsort,
    cos,
    exp,
    floor,
    linspace,
    log10,
    multiply,
    pi,
)
from numpy.fft import fft, fftfreq, fftshift
from scipy import signal


# MWT looks like these are not necessary...
# from ADAR_pyadi_functions import *   #import the ADAR1000 write functions (like ADAR_init and writeBeam functions)
# try:
#     from pluto_config import *    # this has all the key parameters that the user would want to change (i.e. calibration phase and antenna element spacing)
# except:
#     print("Make sure that the file pluto_config_xxxx.py is in the same directory as this python file.")
#     sys.exit(0)
# MWT: Add uri argument...
def SDR_LO_init(
    uri, LO_freq
):  # program the ADF4159 to be the LO of the external LTC555x mixers
    pll = adi.adf4159(uri)
    output_freq = int(LO_freq)
    pll.frequency = int(output_freq / 4)  # Output frequency divided by 4
    BW = 500e6 / 4
    num_steps = 1000
    pll.freq_dev_range = int(
        BW
    )  # frequency deviation range in Hz.  This is the total freq deviation of the complete freq ramp
    pll.freq_dev_step = int(
        BW / num_steps
    )  # frequency deviation step in Hz.  This is fDEV, in Hz.  Can be positive or negative
    pll.freq_dev_time = int(1e3)  # total time (in us) of the complete frequency ramp
    pll.ramp_mode = "disabled"  # ramp_mode can be:  "disabled", "continuous_sawtooth", "continuous_triangular", "single_sawtooth_burst", "single_ramp_burst"
    pll.delay_word = 4095  # 12 bit delay word.  4095*PFD = 40.95 us.  For sawtooth ramps, this is also the length of the Ramp_complete signal
    pll.delay_clk = "PFD"  # can be 'PFD' or 'PFD*CLK1'
    pll.delay_start_en = 0  # delay start
    pll.ramp_delay_en = 0  # delay between ramps.
    pll.trig_delay_en = 0  # triangle delay
    pll.sing_ful_tri = 0  # full triangle enable/disable -- this is used with the single_ramp_burst mode
    pll.tx_trig_en = 0  # start a ramp with TXdata
    # pll.clk1_value = 100
    # pll.phase_value = 3
    pll.enable = 0  # 0 = PLL enable.  Write this last to update all the registers


def SDR_init(
    sdr_address, NumRx, SampleRate, TX_freq, RX_freq, Rx_gain, Tx_gain, buffer_size
):
    """Setup contexts"""
    if NumRx == 1:  # 1 Rx, so this is Pluto
        # sdr=adi.Pluto()     #This finds pluto over usb.  But communicating with its ip address gives us more flexibility
        sdr = adi.Pluto(uri=sdr_address)  # This finds the device at that ip address
    if (
        NumRx == 2
    ):  # 2 Rx, so this is the ADRV9361-SOM or Pluto Rev C (with 2 Rx and 2 Tx enabled)
        sdr = adi.ad9361(uri=sdr_address)
        sdr._ctrl.debug_attrs[
            "adi,frequency-division-duplex-mode-enable"
        ].value = "1"  # move to fdd mode.  see https://github.com/analogdevicesinc/pyadi-iio/blob/ensm-example/examples/ad9361_advanced_ensm.py
        sdr._ctrl.debug_attrs[
            "adi,ensm-enable-txnrx-control-enable"
        ].value = "0"  # Disable pin control so spi can move the states
        sdr._ctrl.debug_attrs["initialize"].value = "1"
        sdr.rx_enabled_channels = [0, 1]  # enable Rx1 (voltage0) and Rx2 (voltage1)
        sdr.gain_control_mode_chan0 = "manual"  # We must be in manual gain control mode (otherwise we won't see the peaks and nulls!)
        sdr.gain_control_mode_chan1 = "manual"  # We must be in manual gain control mode (otherwise we won't see the peaks and nulls!)
    sdr._rxadc.set_kernel_buffers_count(
        1
    )  # Default is 4 Rx buffers are stored, but we want to change and immediately measure the result, so buffers=1
    rx = sdr._ctrl.find_channel("voltage0")
    rx.attrs[
        "quadrature_tracking_en"
    ].value = "1"  # set to '1' to enable quadrature tracking
    sdr.sample_rate = int(SampleRate)
    sdr.rx_lo = int(RX_freq)
    sdr.rx_buffer_size = int(
        buffer_size
    )  # small buffers make the scan faster -- and we're primarily just looking at peak power
    sdr.tx_lo = int(TX_freq)
    sdr.tx_cyclic_buffer = True
    if NumRx == 1:
        sdr.tx_hardwaregain_chan0 = int(
            Tx_gain
        )  # this is a negative number between 0 and -88
        sdr.gain_control_mode_chan0 = "manual"  # We must be in manual gain control mode (otherwise we won't see the peaks and nulls!)
        sdr.rx_hardwaregain_chan0 = int(Rx_gain)
    if NumRx == 2:
        sdr.tx_hardwaregain_chan0 = int(
            -80
        )  # We don't use Tx1, so just make it off or attenuated
        sdr.tx_hardwaregain_chan1 = int(Tx_gain)
        sdr.rx_hardwaregain_chan0 = int(Rx_gain)
        sdr.rx_hardwaregain_chan1 = int(Rx_gain)
    # sdr.filter = "/usr/local/lib/osc/filters/LTE5_MHz.ftr"
    # sdr.rx_rf_bandwidth = int(SampleRate*2)
    # sdr.tx_rf_bandwidth = int(SampleRate*2)
    signal_freq = int(SampleRate / 8)
    if (
        True
    ):  # use either DDS or sdr.tx(iq) to generate the Tx waveform.  But don't do both!
        sdr.dds_enabled = [1, 1, 1, 1, 1, 1, 1, 1]  # DDS generator enable state
        sdr.dds_frequencies = [
            signal_freq,
            0,
            signal_freq,
            0,
            signal_freq,
            0,
            signal_freq,
            0,
        ]  # Frequencies of DDSs in Hz
        sdr.dds_scales = [
            0.5,
            0,
            0.5,
            0,
            0.9,
            0,
            0.9,
            0,
        ]  # Scale of DDS signal generators Ranges [0,1]
    else:
        fs = int(SampleRate)
        N = 1000
        fc = int(signal_freq / (fs / N)) * (fs / N)
        ts = 1 / float(fs)
        t = np.arange(0, N * ts, ts)
        i = np.cos(2 * np.pi * t * fc) * 2 ** 15
        q = np.sin(2 * np.pi * t * fc) * 2 ** 15
        iq = 0.9 * (i + 1j * q)
        sdr.tx([iq, iq])
    return sdr


def SDR_setRx(sdr, NumRx, Rx1_gain, Rx2_gain):
    if NumRx == 1:
        sdr.rx_hardwaregain_chan0 = int(Rx1_gain)
    if NumRx == 2:
        sdr.rx_hardwaregain_chan0 = int(Rx1_gain)
        sdr.rx_hardwaregain_chan1 = int(Rx2_gain)


def SDR_setTx(sdr, NumRx, Tx_gain):
    if NumRx == 1:
        sdr.tx_hardwaregain_chan0 = int(Tx_gain)
    if NumRx == 2:
        sdr.tx_hardwaregain_chan0 = int(
            -80
        )  # We don't use Tx1, so just make it is off or attenuated
        sdr.tx_hardwaregain_chan1 = int(Tx_gain)


def SDR_getData(sdr):
    data = sdr.rx()  # read a buffer of data from Pluto using pyadi-iio library (adi.py)
    return data


def SDR_TxBuffer_Destroy(sdr):
    if sdr.tx_cyclic_buffer == True:
        sdr.tx_destroy_buffer()


def save_hb100_cal(freq, filename="hb100_freq_val.pkl"):
    """ Saves measured frequency calibration file."""
    with open(filename, "wb") as file1:
        pickle.dump(freq, file1)  # save calibrated gain value to a file
        file1.close()


def load_hb100_cal(filename="hb100_freq_val.pkl"):
    """ Load frequency measurement value, set to 10.5GHz if no
        parameters:
            filename: type=string
                      Provide path of gain calibration file
    """
    try:
        with open(filename, "rb") as file1:
            freq = pickle.load(file1)  # Load gain cal values
    except Exception:
        print("file not found, loading default 10.5GHz")
    return freq


def spec_est(x, fs, ref=2 ** 15, plot=False):

    N = len(x)

    # Apply window
    window = signal.kaiser(N, beta=38)
    # x = multiply(x, window)

    # Use FFT to get the amplitude of the spectrum
    ampl = 1 / N * absolute(fft(x))
    ampl = 20 * log10(ampl / ref + 10 ** -20)

    # FFT frequency bins
    freqs = fftfreq(N, 1 / fs)

    # ampl and freqs for real data
    if not np.iscomplexobj(x):
        ampl = ampl[0 : len(ampl) // 2]
        freqs = freqs[0 : len(freqs) // 2]

    if plot:
        # Plot signal, showing how endpoints wrap from one chunk to the next
        import matplotlib.pyplot as plt

        plt.subplot(2, 1, 1)
        plt.plot(x, ".-")
        plt.plot(1, 1, "r.")  # first sample of next chunk
        plt.margins(0.1, 0.1)
        plt.xlabel("Time [s]")
        # Plot shifted data on a shifted axis
        plt.subplot(2, 1, 2)
        plt.plot(fftshift(freqs), fftshift(ampl))
        plt.margins(0.1, 0.1)
        plt.xlabel("Frequency [Hz]")
        plt.tight_layout()
        plt.show()

    return ampl, freqs
