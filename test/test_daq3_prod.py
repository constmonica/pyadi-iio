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
        (5000000, 0.12),
        (10000000, 0.06),
        (10000000, 0.12),
        (15000000, 0.12),
        (15000000, 0.5),
        (200000000, 0.5),
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
