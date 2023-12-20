import adi
import iio
import pytest
import datetime
import hashlib
import subprocess


hardware = ["admv9625", "admv9615"]
classname = ""


###############################################################################

@pytest.mark.iio_hardware(hardware)
@pytest.mark.parametrize("classname", [("adi.mwc")])
@pytest.mark.parametrize(
    "attr, start, stop, step, tol, repeats",
    [
        
        ("tx_autotuning", 1, 0, -1, 0, 1),
        ("rx_autotuning", 1, 0, -1, 0, 1),
        ("tx_auto_ifvga", 1, 0, -1, 0, 1),
        ("rx_auto_ifvga_rflna", 1, 0, -1, 0, 1),
    ],
)

def test_disable_autotuning(test_attribute_single_value, iio_uri, classname, attr, start, stop, step, tol, repeats):
    test_attribute_single_value(iio_uri, classname, attr, start, stop, step, tol, repeats)

########################################

@pytest.mark.iio_hardware(hardware)
@pytest.mark.parametrize("classname", [("adi.hmc6300")])
@pytest.mark.parametrize(
  "attr, start, stop, step, tol, repeats",
  [
        ("vco", 55125000, 66150000, 262500, 100, 1),
        ("if_attn", 10, 15, 1, 100, 1),
        ("rf_attn", 1, 7, 2, 100, 1),
  ],
)

def test_hmc6300(
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
    test_attribute_single_value(iio_uri, classname, attr, start, stop, step, tol, repeats)
    
@pytest.mark.iio_hardware(hardware)
@pytest.mark.parametrize("classname", [("adi.hmc6301")])
@pytest.mark.parametrize(
  "attr, start, stop, step, tol, repeats",
  [
        ("vco", 55125000, 66150000, 262500, 100, 1),
        ("if_attn", 10, 15, 1, 10, 1),
        ("rf_lna_gain", 1, 7, 2, 10, 1),
        ("bb_attn1", 1, 3, 1, 10, 1),
        ("bb_attn2", 1, 3, 1, 10, 1)
  ],
)

def test_hmc6301(
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
    test_attribute_single_value(iio_uri, classname, attr, start, stop, step, tol, repeats)

############################################################
    
@pytest.mark.iio_hardware(hardware)
@pytest.mark.parametrize("classname", [("adi.max24287")])
@pytest.mark.parametrize(
    "attr, start, stop, step, tol, repeats",
    [
        ("par_speed", 1, 5, 2, 1, 1),
        ("ser_link", 0, 5, 1, 10, 1),
        ("ser_speed", 0, 1, 1, 100, 1)
    ],
)

def test_max24287(test_attribute_single_value, iio_uri, classname, attr, start, stop, step, tol, repeats):
    test_attribute_single_value(iio_uri, classname, attr, start, stop, step, tol, repeats)
    
@pytest.mark.iio_hardware(hardware)
@pytest.mark.parametrize("classname", [("adi.adin1300")])
@pytest.mark.parametrize(
    "attr, start, stop, step, tol, repeats",
    [
        ("link", 0, 1, 1, 10, 1),
        ("speed", 0, 5, 1, 10, 1),
    ],
)

def test_adin1300(test_attribute_single_value, iio_uri, classname, attr, start, stop, step, tol, repeats):
    test_attribute_single_value(iio_uri, classname, attr, start, stop, step, tol, repeats)
    
@pytest.mark.iio_hardware(hardware)
@pytest.mark.parametrize("classname", [("adi.mwc")])
@pytest.mark.parametrize(
    "attr, start, stop, step, tol, repeats",
    [
        ("tx_target", 100, 400, 10, 10, 1),
        ("rx_target", 1800, 2050, 100, 10, 1),
        ("tx_det", 300, 400, 10, 10, 1),
        ("rx_det", 600, 900, 10, 10, 1),
        ("rx_tolerance", 1800, 2050, 100, 10, 1)
    ],
)

def test_mwc(test_attribute_single_value, iio_uri, classname, attr, start, stop, step, tol, repeats):
    test_attribute_single_value(iio_uri, classname, attr, start, stop, step, tol, repeats)




##################### READING CURRENT0 ATTRIBUTE ###################


adm1177 = adi.adm1177(uri="serial:/dev/ttyACM0,345600,8n1n")


@pytest.mark.iio_hardware(hardware)
@pytest.mark.parametrize("classname", [("adi.adm1177")])
@pytest.mark.parametrize("channel", ["current0"])
@pytest.mark.parametrize(
    "attr, start, stop, step, tol, repeats",
    [
        ("raw", 250, 450, 1, 10, 10),
        ("scale", 1, 2, 0.5, 10, 10),
    ],
)

def test_current(test_attribute_single_value, iio_uri, classname, attr, start, stop, step, tol, repeats, channel):
    test_attribute_single_value(iio_uri, classname, attr, start, stop, step, tol, repeats, channel)
    current_channel = adm1177.current0(adm1177._ctrl, "current0")
    current_channel.calculate_current()










