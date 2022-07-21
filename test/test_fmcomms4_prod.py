import iio

import adi
import numpy as np
import pytest

hardware = ["packrf", "adrv9364", "fmcomms4", "ad9364"]
classname = "adi.ad9364"

##################################
@pytest.mark.iio_hardware(hardware)
@pytest.mark.parametrize(
    "voltage_raw, low, high",
    [
        ("in_temp0", 20, 50),
        ("in_voltage0", 2129, 2713),
        ("in_voltage1", 2129, 2713),
        ("in_voltage2", 2948, 3532),
        ("in_voltage3", 2048, 2632),
        ("in_voltage4", 1064, 1648),
        ("in_voltage5", 1064, 1648),
    ],
)
def test_ad7291(context_desc, voltage_raw, low, high):
    ctx = None
    for ctx_desc in context_desc:
        if ctx_desc["hw"] in hardware:
            ctx = iio.Context(ctx_desc["uri"])
    if not ctx:
        pytest.skip("No valid hardware found")

    ad7291 = ctx.find_device("ad7291")

    for channel in ad7291.channels:
        c_name = "out" if channel.output else "in"
        c_name += "_" + str(channel.id)
        if c_name == voltage_raw:
            for attr in channel.attrs:
                if attr == "raw":
                    if c_name == "in_temp0":
                        temp = (2.5 * (int(channel.attrs[attr].value)/10 + 109.3) - 273.15)
                        print(temp)
                        assert low <= temp <= high
                    else:
                        try:
                            print(channel.attrs[attr].value)
                            assert low <= int(channel.attrs[attr].value) <= high
                        except OSError:
                            continue


@pytest.mark.iio_hardware(hardware)
@pytest.mark.parametrize("classname", [(classname)])
@pytest.mark.parametrize(
    "attr, start, stop, step, tol, repeats",
    [
        ("rx_lo", 2300000000, 2500000000, 1, 8, 10),
        ("tx_lo", 1300000000, 2500000000, 1, 8, 10),
    ]
)
def test_ad9364_attr(
    test_attribute_single_value,
    iio_uri,
    classname,
    attr,
    start,
    stop,
    step,
    tol,
    repeats,
):
    test_attribute_single_value(
        iio_uri, classname, attr, start, stop, step, tol, repeats
    )


@pytest.mark.iio_hardware(hardware)
@pytest.mark.parametrize("classname", [(classname)])
@pytest.mark.parametrize("channel", [0])
@pytest.mark.parametrize(
    "dds_scale, min_rssi, max_rssi, param_set",
    [
        (
            0.0,
            80,
            150,
            dict(
                rx_rf_port_select="A_BALANCED",
                tx_rf_port_select="A",
                sample_rate=30720000,
                tx_lo=1450000000,
                rx_lo=2749999996,
                tx_hardwaregain_chan0=-10,
                gain_control_mode_chan0="slow_attack",
                rx_rf_bandwidth=18000000,
                tx_rf_bandwidth=18000000,
            ),
        ),
        (
            0.0,
            75,
            150,
            dict(
                rx_rf_port_select="B_BALANCED",
                tx_rf_port_select="B",
                sample_rate=30720000,
                tx_lo=1400000000,
                rx_lo=2749999996,
            ),
        ),
        (
            0.1,
            20,
            50,
            dict(
                rx_rf_port_select="A_BALANCED",
                tx_rf_port_select="A",
                gain_control_mode_chan0="slow_attack",
                rx_lo=2749999996,
                tx_lo=2750000000,
               
            ),
        ),
        (
            0.1,
            10,
            50,
            dict(
                rx_rf_port_select="B_BALANCED",
                tx_rf_port_select="B",
                gain_control_mode_chan0="slow_attack",
                rx_lo=2749999996,
                tx_lo=2750000000,
            ),
        ),
    ],
)
def test_rssi(
    test_gain_check,
    iio_uri,
    classname,
    channel,
    param_set,
    dds_scale,
    min_rssi,
    max_rssi,
):
    test_gain_check(
        iio_uri, classname, channel, param_set, dds_scale, min_rssi, max_rssi
    )


@pytest.mark.iio_hardware(hardware)
@pytest.mark.parametrize("classname", [(classname)])
@pytest.mark.parametrize("channel", [0])
@pytest.mark.parametrize(
    "dds_scale, frequency, hardwaregain_low, hardwaregain_high, param_set",
    [
        (
            0.0,
            999859,
            60,
            80,
            dict(
                rx_rf_port_select="A_BALANCED",
                tx_rf_port_select="A",
                gain_control_mode_chan0="slow_attack",
                rx_lo=1400000000,
                tx_lo=2750000000,
            ),
        ),
        (
            0.0,
            999859,
            50,
            80,
            dict(
                rx_rf_port_select="B_BALANCED",
                tx_rf_port_select="B",
                gain_control_mode_chan0="slow_attack",
                rx_lo=1400000000,
                tx_lo=2750000000,
            ),
        ),
        (
            0.4,
            999859,
            0.0,
            25,
            dict(
                rx_rf_port_select="A_BALANCED",
                tx_rf_port_select="A",
                gain_control_mode_chan0="slow_attack",
                rx_lo=2749999996,
                tx_lo=2750000000,
            ),
        ),
        (
            0.4,
            999859,
            0.0,
            28,
            dict(
                rx_rf_port_select="B_BALANCED",
                tx_rf_port_select="B",
                gain_control_mode_chan0="slow_attack",
                rx_lo=2749999996,
                tx_lo=2750000000,
            ),
        )
    ],
)
def test_hardware_gain(
    test_hardwaregain,
    iio_uri,
    classname,
    channel,
    dds_scale,
    frequency,
    hardwaregain_low,
    hardwaregain_high,
    param_set,
):
    test_hardwaregain(
        iio_uri,
        classname,
        channel,
        dds_scale,
        frequency,
        hardwaregain_low,
        hardwaregain_high,
        param_set,
    )


@pytest.mark.iio_hardware(hardware)
@pytest.mark.parametrize("classname", [(classname)])
@pytest.mark.parametrize("channel", [0])
def test_ad9364_loopback(test_dma_loopback, iio_uri, classname, channel):
    test_dma_loopback(iio_uri, classname, channel)


@pytest.mark.iio_hardware(hardware)
@pytest.mark.parametrize("classname", [(classname)])
@pytest.mark.parametrize("channel", [0])
@pytest.mark.parametrize(
    "param_set",
    [
        dict(
            rx_rf_port_select="A_BALANCED",
            tx_rf_port_select="A",
            sample_rate=30720000,
            rx_lo=3000000000,
            tx_lo=3000000000,
            gain_control_mode_chan0="slow_attack",
        ),
        dict(
            rx_rf_port_select="B_BALANCED",
            tx_rf_port_select="B",
            sample_rate=30720000,
            rx_lo=3000000000,
            tx_lo=3000000000,
            gain_control_mode_chan0="slow_attack",
        ),
    ],
)
def test_ad9364_iq_loopback(test_iq_loopback, iio_uri, classname, channel, param_set):
    test_iq_loopback(iio_uri, classname, channel, param_set)


@pytest.mark.iio_hardware(hardware)
@pytest.mark.parametrize("classname", [(classname)])
@pytest.mark.parametrize("channel", [0])
@pytest.mark.parametrize(
    "param_set",
    [
        dict(
            rx_rf_port_select="A_BALANCED",
            tx_rf_port_select="A",
            rx_lo=3000000000,
            tx_lo=3000000000,
        ),
        dict(
            rx_rf_port_select="B_BALANCED",
            tx_rf_port_select="B",
            rx_lo=2600000000,
            tx_lo=2600000000,
        ),
    ],
)
@pytest.mark.parametrize(
    "low, high",
    [([-20.0, -120.0, -120.0, -125.0], [-10.0, -75.0, -75.0, -80.0])],
)
def test_harmonic_values(
    test_harmonics, classname, iio_uri, channel, param_set, low, high, plot=False
):
    test_harmonics(classname, iio_uri, channel, param_set, low, high, plot)


@pytest.mark.iio_hardware(hardware)
@pytest.mark.parametrize("classname", [(classname)])
@pytest.mark.parametrize("channel", [0])
@pytest.mark.parametrize(
    "param_set",
    [
        dict(
            rx_rf_port_select="A_BALANCED",
            tx_rf_port_select="A",
            rx_lo=3000000000,
            tx_lo=3000000000,
        ),
        dict(
            rx_rf_port_select="B_BALANCED",
            tx_rf_port_select="B",
            rx_lo=2600000000,
            tx_lo=2600000000,
        ),
    ],
)
@pytest.mark.parametrize(
    "low, high",
    [([-20.0, -120.0, -120.0, -125.0], [-10.0, -70.0, -70.0, -75.0])],
)
def test_peaks(test_sfdrl, classname, iio_uri, channel, param_set, low, high, plot=False):
    test_sfdrl(classname, iio_uri, channel, param_set, low, high, plot=False)
