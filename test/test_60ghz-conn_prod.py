import adi
import iio
import pytest


hardware = "admv9625"
classname = ""



########################################

@pytest.mark.iio_hardware("admv9625")
@pytest.mark.parametrize("classname", [("adi.hmc6300")])
@pytest.mark.parametrize(
  "attr, start, stop, step, tol, repeats",
  [
        ("vco", 55125000, 66150000, 262500, 10000, 1),
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
    
@pytest.mark.iio_hardware("admv9625")
@pytest.mark.parametrize("classname", [("adi.hmc6301")])
@pytest.mark.parametrize(
  "attr, start, stop, step, tol, repeats",
  [
        ("vco", 55125000, 66150000, 262500, 10000, 1),
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
    
@pytest.mark.iio_hardware("admv9625")
@pytest.mark.parametrize("classname", [("adi.max24287")])
@pytest.mark.parametrize(
    "attr, start, stop, step, tol, repeats",
    [
        ("par_speed", 0, 5, 1, 10, 1),
        ("ser_link", 0, 5, 1, 10, 1),
        ("ser_speed", 0, 1, 1, 10, 1)
    ],
)

def test_max24287(test_attribute_single_value, iio_uri, classname, attr, start, stop, step, tol, repeats):
    test_attribute_single_value(iio_uri, classname, attr, start, stop, step, tol, repeats)
    
@pytest.mark.iio_hardware("admv9625")
@pytest.mark.parametrize("classname", [("adi.adin1300")])
@pytest.mark.parametrize(
    "attr, start, stop, step, tol, repeats",
    [
        ("link", 0, 1, 1, 10, 1),
        ("speed", 0, 5, 1, 10, 1),
        # ("direct_reg_access", 2000, 4500, 100, 10, 2)
    ],
)

def test_adin1300(test_attribute_single_value, iio_uri, classname, attr, start, stop, step, tol, repeats):
    test_attribute_single_value(iio_uri, classname, attr, start, stop, step, tol, repeats)
    
@pytest.mark.iio_hardware("admv9625")
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















