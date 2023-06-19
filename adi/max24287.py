from collections import OrderedDict
from adi.attribute import attribute
from adi.context_manager import context_manager
from decimal import *

class max24287(context_manager, attribute):
    _det_channel = []
    
    _complex_data = False
    channel = [] 
    _device_name = "max24287"
    
    
    # Get the context
    def __init__(self, uri="", device_name="max24287"):

        context_manager.__init__(self, uri, self._device_name)

        self._ctrl = None
        
        #Select the device matching device_name as working device
        
        for device in self._ctx.devices:
            print("Found device {}".format(device_name))
            if device.name == device_name:
                self._ctrl = device
                break
    

    @property
    def par_speed(self):
        return self._get_iio_dev_attr("par_speed")
    
    @par_speed.setter
    def par_speed(self, value):
        self._set_iio_dev_attr("par_speed", value)

    @property
    def ser_link(self):
        return self._get_iio_dev_attr("ser_link")
    
    @ser_link.setter
    def ser_link(self, value):
        self._set_iio_dev_attr("ser_link", "1" if value else "0")

    @property
    def ser_speed(self):
        return self._get_iio_dev_attr("ser_speed")
    
    @ser_speed.setter
    def ser_speed(self, value):
        self._set_iio_dev_attr("ser_speed", value)

    @property
    def direct_reg_access(self):
        return self._get_iio_debug_attr("direct_reg_access")

    @direct_reg_access.setter
    def direct_reg_access(self, value):
        self._set_iio_debug_attr_str('direct_reg_access', value)