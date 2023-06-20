# Copyright (C) 2023 Analog Devices, Inc.
#
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
#     - Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     - Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in
#       the documentation and/or other materials provided with the
#       distribution.
#     - Neither the name of Analog Devices, Inc. nor the names of its
#       contributors may be used to endorse or promote products derived
#       from this software without specific prior written permission.
#     - The use of this software may or may not infringe the patent rights
#       of one or more patent holders.  This license does not release you
#       from the requirement that you obtain separate licenses from these
#       patent holders to use this software.
#     - Use of the software either in source or binary form, must be run
#       on or directly connected to an Analog Devices Inc. component.
#
# THIS SOFTWARE IS PROVIDED BY ANALOG DEVICES "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
# INCLUDING, BUT NOT LIMITED TO, NON-INFRINGEMENT, MERCHANTABILITY AND FITNESS FOR A
# PARTICULAR PURPOSE ARE DISCLAIMED.
#
# IN NO EVENT SHALL ANALOG DEVICES BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, INTELLECTUAL PROPERTY
# RIGHTS, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR
# BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
# STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF
# THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


from collections import OrderedDict
from adi.attribute import attribute
from adi.context_manager import context_manager
from decimal import *

class hmc6300(context_manager, attribute):
    _temp_channel = []

    _complex_data = False
    channel = []
    _device_name ="hmc6300"

    # Get the context 
    def __init__(self, uri="", device_name="hmc6300"):
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
    def rf_attn(self):
        return self._get_iio_dev_attr("rf_attn")
    
    @rf_attn.setter
    def rf_attn(self, value):
        self._set_iio_dev_attr("rf_attn", value)
    
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
        
    