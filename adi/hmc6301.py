from collections import OrderedDict
from adi.attribute import attribute
from adi.context_manager import context_manager
from decimal import *

class hmc6301(context_manager, attribute):
    _temp_channel = []

    _complex_data = False
    channel = []
    _device_name ="hmc6301"

    # Get the context 
    def __init__(self, uri="", device_name="hmc6301"):
        context_manager.__init__(self, uri, self._device_name)
        self._ctrl = None

    # Select the device matching device name as working device

        for device in self._ctx.devices:
            print("Found device {}".format(device_name))
            if device.name == device_name:
                self._ctrl = device
                break
    
    # Dinamically get channels

        _channels = []
        for ch in self._ctrl.channels:
            self._temp_channel.append(ch.id)
            if "temp" == ch.id:
                _channels.append((ch.id, self.temp(self._ctrl, ch.id)))
                continue
        self.channel = OrderedDict(_channels)

    # Device specific attributes

    @property
    def enabled(self):
        return self._get_iio_dev_attr("enabled")
    
    @enabled.setter
    def enabled(self, value):
        self._set_iio_dev_attr("enabled", "1" if value else "0")
    
    @property
    def vco(self):
        return self._get_iio_dev_attr("vco")
    
    @vco.setter
    def vco(self, value):
        self._set_iio_dev_attr("vco", value)

    @property
    def vco_available(self):
        return self._get_iio_dev_attr("vco_available")
    
    @vco_available.setter
    def vco_available(self, value):
        self._set_iio_dev_attr("vco_available", value)
    
    @property
    def if_attn(self):
        return self._get_iio_dev_attr("if_attn")
    
    @if_attn.setter
    def if_attn(self, value):
        self._set_iio_dev_attr("if_attn", value)

    @property
    def temp_en(self):
        return self._get_iio_dev_attr("temp_en")
    
    @temp_en.setter
    def temp_en(self, value):
        self._set_iio_dev_attr("temp_en", "1" if value else "0")
    
    @property
    def rf_lna_gain(self):
        return self._get_iio_dev_attr("rf_lna_gain")
    
    @rf_lna_gain.setter
    def rf_lna_gain(self, value):
        self._set_iio_dev_attr("rf_attn", value)

    @property
    def bb_attn1(self):
        return self._get_iio_dev_attr("bb_attn1")
    
    @bb_attn1.setter
    def bb_attn1(self, value):
        self._set_iio_dev_attr("bb_attn1", value)

    @property
    def bb_attn2(self):
        return self._get_iio_dev_attr("bb_attn2")
    
    @bb_attn1.setter
    def bb_attn2(self, value):
        self._set_iio_dev_attr("bb_attn2", value)

    @property
    def bb_attni_fine(self):
        return self._get_iio_dev_attr("bb_attni_fine")
    
    @bb_attn1.setter
    def bb_attni_fine(self, value):
        self._set_iio_dev_attr("bb_attni_fine", value)
    
    @property
    def bb_attnq_fine(self):
        return self._get_iio_dev_attr("bb_attnq_fine")
    
    @bb_attn1.setter
    def bb_attnq_fine(self, value):
        self._set_iio_dev_attr("bb_attnq_fine", value)

    @property
    def bb_lpc(self):
        return self._get_iio_dev_attr("bb_lpc")
    
    @bb_attn1.setter
    def bb_lpc(self, value):
        self._set_iio_dev_attr("bb_lpc", value)


    @property
    def bb_hpc(self):
        return self._get_iio_dev_attr("bb_hpc")
    
    @bb_attn1.setter
    def bb_hpc(self, value):
        self._set_iio_dev_attr("bb_hpc", value)


    
    @property
    def direct_reg_access(self):
        return self._get_iio_debug_attr("direct_reg_access")
    
    @direct_reg_access.setter
    def direct_reg_access(self, value):
        self._set_iio_debug_attr_str("direct_reg_access", value)

    class temp(attribute):
        def __init__(self, ctrl, channel_name):
            self.name = channel_name
            self._ctrl = ctrl

        @property
        def raw(self):
            return self._get_iio_attr(self.name, "raw", False)
        
    