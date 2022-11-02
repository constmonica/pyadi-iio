import iio

import adi
import numpy as np
import pytest

hardware = "daq3"
classname = "adi.DAQ3"


##################################
@pytest.mark.iio_hardware(hardware)
@pytest.mark.parametrize(
    "voltage_raw, low, high",
    [
        ("in_temp0", 40, 60),
        ("in_voltage0", 2703, 3296),
        ("in_voltage1", 2540, 2867),
        ("in_voltage2", 2540, 2867),
        ("in_voltage3", 1229, 1393),
        ("in_voltage4", 1884, 2179),
        ("in_voltage5", 2458, 2867),
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



#########################################
@pytest.mark.iio_hardware(hardware)
@pytest.mark.parametrize("classname", [(classname)])
@pytest.mark.parametrize("channel", [0, 1, [0, 1]])
def test_daq3_tx_data(test_dma_tx, iio_uri, classname, channel):
    test_dma_tx(iio_uri, classname, channel)


#########################################
@pytest.mark.iio_hardware(hardware)
@pytest.mark.parametrize("classname", [(classname)])
@pytest.mark.parametrize("channel", [0, 1, [0, 1]])
def test_daq3_rx_data(test_dma_rx, iio_uri, classname, channel):
    test_dma_rx(iio_uri, classname, channel)


#########################################
@pytest.mark.iio_hardware(hardware)
@pytest.mark.parametrize("classname", [(classname)])
@pytest.mark.parametrize("channel", [0, 1])
@pytest.mark.parametrize("param_set", [dict()])
@pytest.mark.parametrize(
    "frequency, scale",
    [
        (97001602, 0.12),
        (97001602, 0.06),
        (39993896, 0.12),
        (39993896, 0.12),
    ],
)
@pytest.mark.parametrize("peak_min", [-45])
def test_daq3_dds_loopback(
    test_dds_loopback,
    iio_uri,
    classname,
    param_set,
    channel,
    frequency,
    scale,
    peak_min,
):
    test_dds_loopback(
        iio_uri, classname, param_set, channel, frequency, scale, peak_min
    )


#########################################
@pytest.mark.iio_hardware(hardware)
@pytest.mark.parametrize("classname", [(classname)])
@pytest.mark.parametrize("channel", [0, 1])
@pytest.mark.parametrize("param_set", [dict()])
def test_daq3_cw_loopback(test_cw_loopback, iio_uri, classname, channel, param_set):
    test_cw_loopback(iio_uri, classname, channel, param_set)

# @pytest.mark.iio_hardware(hardware)
# @pytest.mark.parametrize("classname", [(classname)])
# @pytest.mark.parametrize("channel", [0, 1])
# @pytest.mark.parametrize(
#     "dds_scale, min_rssi, max_rssi, param_set",
#     [
#         (
#             0.0,
#             75,
#             150,
#             dict(
#                 sample_rate=1233333333,
#                 tx_lo=2400000000,
#                 rx_lo=2400000000,
#                 gain_control_mode_chan0="slow_attack",
#                 gain_control_mode_chan1="slow_attack",
#                 rx_rf_bandwidth=18000000,
#                 tx_rf_bandwidth=18000000,
#             ),
#         ),
#         (
#             0.4,
#             10,
#             50,
#             dict(
#                 gain_control_mode_chan0="slow_attack",
#                 gain_control_mode_chan1="slow_attack",
#                 rx_lo=2400000000,
#                 tx_lo=2400000000,
#                 tx_hardwaregain_chan0=-10,
#                 tx_hardwaregain_chan1=-10,
#                 sample_rate=1233333333,
#                 rx_rf_bandwidth=18000000,
#                 tx_rf_bandwidth=18000000,
#             ),
#         ),
#     ],
# )

# def test_rssi(
#     test_gain_check,
#     iio_uri,
#     classname,
#     channel,
#     param_set,
#     dds_scale,
#     min_rssi,
#     max_rssi,
# ):
#     test_gain_check(
#         iio_uri, classname, channel, param_set, dds_scale, min_rssi, max_rssi
#     )

# @pytest.mark.iio_hardware(hardware)
# @pytest.mark.parametrize("classname", [(classname)])
# @pytest.mark.parametrize("channel", [0])
# @pytest.mark.parametrize(
#     "dds_scale, frequency, hardwaregain_low, hardwaregain_high, param_set",
#     [
#         (
#             0.0,
#             999859,
#             50,
#             80,
#             dict(
#                 rx_rf_port_select="A_BALANCED",
#                 tx_rf_port_select="A",
#                 gain_control_mode_chan0="slow_attack",
#                 rx_lo=1400000000,
#                 tx_lo=2750000000,
#             ),
#         ),
#         (
#             0.0,
#             999859,
#             50,
#             80,
#             dict(
#                 rx_rf_port_select="B_BALANCED",
#                 tx_rf_port_select="B",
#                 gain_control_mode_chan0="slow_attack",
#                 rx_lo=1400000000,
#                 tx_lo=2750000000,
#             ),
#         ),
#         (
#             0.4,
#             999859,
#             0.0,
#             25,
#             dict(
#                 rx_rf_port_select="A_BALANCED",
#                 tx_rf_port_select="A",
#                 gain_control_mode_chan0="slow_attack",
#                 rx_lo=2749999996,
#                 tx_lo=2750000000,
#             ),
#         ),
#         (
#             0.4,
#             999859,
#             0.0,
#             28,
#             dict(
#                 rx_rf_port_select="B_BALANCED",
#                 tx_rf_port_select="B",
#                 gain_control_mode_chan0="slow_attack",
#                 rx_lo=2749999996,
#                 tx_lo=2750000000,
#             ),
#         )
#     ],
# )
# def test_hardware_gain(
#     test_hardwaregain,
#     iio_uri,
#     classname,
#     channel,
#     dds_scale,
#     frequency,
#     hardwaregain_low,
#     hardwaregain_high,
#     param_set,
# ):
#     test_hardwaregain(
#         iio_uri,
#         classname,
#         channel,
#         dds_scale,
#         frequency,
#         hardwaregain_low,
#         hardwaregain_high,
#         param_set,
#     )

@pytest.mark.iio_hardware(hardware)
@pytest.mark.parametrize("classname", [(classname)])
@pytest.mark.parametrize("channel", [0, 1])
@pytest.mark.parametrize(
    "param_set",
    [
        dict(
            sample_rate=1233333333,
            rx_lo=2400000000,
            tx_lo=2400000000,
        ),
        dict(
            sample_rate=1233333333,
            rx_lo=2400000000,
            tx_lo=2400000000,
        ),
    ],
)
@pytest.mark.parametrize(
    "low, high",
    [([-20.0, -150.0, -150.0, -150.0], [0.0, -67.0, -55.0, -72.0])],
)
@pytest.mark.parametrize(
    "dds_freq",
    [97014318, 185014114, 169996185],
)
def test_harmonic_values(
    test_harmonics, classname, iio_uri, channel, param_set, low, high, dds_freq, plot=False
):
    test_harmonics(classname, iio_uri, channel, param_set, low, high, dds_freq, plot)