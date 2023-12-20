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

class adm1177(context_manager, attribute):
    
    _complex_data = False
    channel = []
    _device_name = "adm1177"
    
    # Get the context
    def __init__(self, uri="", device_name="adm1177"):

        context_manager.__init__(self, uri, self._device_name)

        self._ctrl = None
        
        #Select the device matching device_name as working device
        
        for device in self._ctx.devices:
            if device.name == device_name:
                #print("Found device {}".format(device_name))
                self._ctrl = device
                break
            
    # Dinamically get channels

        _channels = []
        for ch in self._ctrl.channels:
            self.channel.append(ch.id)
            if "current0" == ch.id:
                _channels.append(ch.id)
                continue
#         self.channel = OrderedDict(_channels)
        
        
        
    class current0(attribute):
        def __init__(self, ctrl, channel_name):
            self.name = channel_name
            self._ctrl = ctrl

        @property
        def raw(self):
            return self._get_iio_attr(self.name, "raw", False)
        
        @property
        def scale(self):
            return self._get_iio_attr(self.name, "scale", False)
        
        def calculate_current(self):
            raw = self.raw
            scale = self.scale
            # current = raw * scale
            num_measurements = 10
            total_current = 0
            
            for _ in range(num_measurements):
                current = self.raw * self.scale
                total_current += current
                # print(f"Current is: {current} mA.")
            average = total_current / num_measurements
            average_current = round(average, 2)
            print(f"Average Current is: {average_current} mA.")
                        
            if average_current < 320:
                raise ValueError("Average current is below the desired minimum of 350 mA.")
            elif 320 <= average_current <= 420:
                print("Average current is within the desired range.")
            else:
                print("Average current is above the desired maximum of 450 mA.")
                exit()
                
                
                
            