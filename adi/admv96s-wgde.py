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

class mwc(context_manager, attribute):
    _det_channel = []
    
    _complex_data = False
    channel = [] 
    _device_name = "mwc"
    
    
    # Get the context
    def __init__(self, uri="", device_name="mwc"):

        context_manager.__init__(self, uri, self._device_name)

        self._ctrl = None
        
        #Select the device matching device_name as working device
        
        for device in self._ctx.devices:
            print("Found device {}".format(device_name))
            if device.name == device_name:
                self._ctrl = device
                break
        
        # Dynamically get channels
        
        _channels = []
        for ch in self._ctrl.channels:
            self._det_channel.append(ch.id)
            if "voltage1" == ch.id:
                _channels.append((ch.id, self.rx_det(self._ctrl, ch.id)))
                continue
            if "voltage0" == ch.id:
                _channels.append((ch.id, self.tx_det(self._ctrl, ch.id)))
                continue
        self.channel = OrderedDict(_channels)
        
    # Device specific attributes

    @property
    def tx_autotuning(self):
        return self._get_iio_dev_attr("tx_autotuning")
       
    @tx_autotuning.setter
    def tx_autotuning(self, value):
        self._set_iio_dev_attr("tx_autotuning", "1" if value else "0")

    @property
    def tx_target(self):
        return self._get_iio_dev_attr("tx_target")
    
    @tx_target.setter
    def tx_target(self, value):
        self._set_iio_dev_attr("tx_target", value)
    
    @property
    def tx_tolerance(self):
        return self._get_iio_dev_attr("tx_tolerance", self._ctrl) 

    @tx_tolerance.setter
    def tx_tolerance(self, value):
        self._set_iio_dev_attr("tx_tolerance", value)
        
    @property
    def rx_autotuning(self):
        return self._get_iio_dev_attr("rx_autotuning")
        
    @rx_autotuning.setter
    def rx_autotuning(self, value):
        self._set_iio_dev_attr("rx_autotuning", "1" if value else "0")
            
    @property
    def rx_target(self):
        return self._get_iio_dev_attr("rx_target")
        
    @rx_target.setter
    def rx_target(self, value):
        self._set_iio_dev_attr("rx_target", value)
        
    @property
    def rx_tolerance(self):
        return self._get_iio_dev_attr("rx_tolerance", self._ctrl)
        
    @rx_tolerance.setter
    def rx_tolerance(self, value):
        self._set_iio_dev_attr("rx_tolerance", value)
        
    @property
    def tx_auto_ifvga(self):
        return self._get_iio_dev_attr("tx_auto_ifvga", False)
        
    @tx_auto_ifvga.setter
    def tx_auto_ifvga(self, value):
        self._set_iio_attr("tx_auto_ifvga", "1" if value else "0")
            
    @property
    def rx_auto_ifvga_rflna(self):
        return self._get_iio_dev_attr("rx_auto_ifvga_rflna", self._ctrl)
    
    @rx_auto_ifvga_rflna.setter
    def rx_auto_ifvga_rflna(self, value):
        self._set_iio_attr("rx_auto_ifvga_rflna", "1" if value else "0")
        
    @property
    def reset(self):
        """ Reset MWC to default settings"""
        self._set_iio_dev_attr("reset", 1, self._ctrl)


    # Tx det channel and attributes

    class tx_det(attribute):
        def __init__(self, ctrl, channel_name):
            self.name = channel_name
            self._ctrl = ctrl

        @property
        def raw(self):
            """MWC tx channel raw value"""        
            return self._get_iio_attr(self.name, "raw", False)

        @property
        def scale(self):
            """MWC tx channel scale value"""
            return float(self._get_iio_attr(self.name, "scale", False))

    # RX det channel and attributes

    class rx_det(attribute):
        def __init__(self, ctrl, channel_name):
            self.name = channel_name
            self._ctrl = ctrl

        @property
        def raw(self):
            """MWC rx channel raw value"""        
            return self._get_iio_attr(self.name, "raw", False)

        @property
        def scale(self):
            """MWC rx channel scale value"""
            print(self.name)
            return float(self._get_iio_attr(self.name, "scale", False))
        
        #Function to return voltage
        def __call__(self):
            """Utility function, returns milivolts"""
            return self.raw * self.scale
        