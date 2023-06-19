from collections import OrderedDict
from adi.attribute import attribute
from adi.context_manager import context_manager
from decimal import *

class adin1300(context_manager, attribute):
    
    _complex_data = False
    channel = [] 
    _device_name = "adin1300"
    
    
    # Get the context
    def __init__(self, uri="", device_name="adin1300"):

        context_manager.__init__(self, uri, self._device_name)

        self._ctrl = None
        
        #Select the device matching device_name as working device
        
        for device in self._ctx.devices:
            print("Found device {}".format(device_name))
            if device.name == device_name:
                self._ctrl = device
                break

    @property
    def link(self):
        return self._get_iio_dev_attr("link")
    
    @link.setter
    def link(self, value):
        self._set_iio_dev_attr("link", value)
    
    @property
    def speed(self):
        return self._get_iio_dev_attr("speed")
    
    @speed.setter
    def speed(self, value):
        self._set_iio_dev_attr("speed", value)

    @property
    def autonegotiate(self):
        return self._get_iio_dev_attr("autonegotiate")
    
    @autonegotiate.setter
    def autonegotiate(self, value):
        self._set_iio_dev_attr("autonegotiate", "1" if value else "0")

    @property
    def direct_reg_access(self):
        return self._get_iio_debug_attr("direct_reg_access")
    
    @direct_reg_access.setter
    def direct_reg_access(self, value):
        self._set_iio_debug_attr_str("direct_reg_access", value)