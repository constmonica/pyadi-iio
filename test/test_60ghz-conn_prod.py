import adi
import iio
import pytest
import datetime
import hashlib
import subprocess


hardware = ["admv9625", "admv9615"]
classname = ""

# ########################### SERIAL NUMBER WRITING #############################

@pytest.mark.iio_hardware(hardware)
@pytest.mark.parametrize("classname", [("adi.mwc")])
@pytest.mark.parametrize("attr", [("carrier_serial")])
@pytest.mark.parametrize("val", [("val")])

def test_write_serial_attr(test_attribute_single_value_str, iio_uri, classname, attr, val):
    date_string = datetime.datetime.now().strftime('%y%m%d')
    hash_string = hashlib.md5(str(datetime.datetime.now().time().microsecond).encode()).hexdigest()[:7]
    val = f"{date_string}-{hash_string}"
    test_attribute_single_value_str(iio_uri, classname, attr, val, 0)
# 

# ################################# WRITING SAVE AND SAVE DEFAULTS STATE VARIABLE ##############
@pytest.mark.iio_hardware(hardware)
@pytest.mark.parametrize("classname", [("adi.mwc")])
@pytest.mark.parametrize("attr, val",
                         [
                             ("save", "1"),
                             ("save_defaults", "1"),
                             ("hw_version", "-"),
                             ("hw_serial", "-"),
                             ("carrier_version", "b"),
                             ("carrier_model", "admv96s-wghe-ek")
                            
                            ],
                         )
def test_write_save(test_attribute_write_only_str, iio_uri, classname, attr, val):
    test_attribute_write_only_str(iio_uri, classname, attr, val)



                                 
                                 
# ###################################### READING FIRMWARE VERSION ATTR ################################

def check_firmware(word):
    command = "sudo iio_info -u serial:/dev/ttyACM0,345600,8n1n | grep 'Backend description string'"

    try:
        output = subprocess.check_output(command, shell=True, text=True)
        lines = output.strip().split('\n')
        last_line = lines[-1] if lines else None

        return word in last_line if last_line else False
    except subprocess.CalledProcessError as e:
        print(f"Error executing the command: {e}")
        return False

@pytest.mark.parametrize("word_to_check, expected_result", [
    ("wethlink-production", True)])

def test_check_firmware(word_to_check, expected_result):
    assert check_firmware(word_to_check) == expected_result
















