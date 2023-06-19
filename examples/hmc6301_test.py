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

import sys
from time import sleep
import adi


# Set up HMC6301 device
#dev = adi.mwc(uri="serial:/dev/ttyACM0,115200,8n2n") 
hmc6301 = adi.hmc6301(uri="ip:127.0.0.1")

# Device attributes
hmc6301.enabled = True
print("Enabled value:", hmc6301.enabled)
#dev.vco = 100000
print("vco", hmc6301.vco)
print("vco_available=:", hmc6301.vco_available)
#dev.if_attn = 18
print("if attenuation", hmc6301.if_attn)
#dev.temp_en = False
print("temperature enable:", hmc6301.temp_en)
print("rf_attn", hmc6301.rf_lna_gain)
#dev.direct_reg_access = 19
print("debug attr:", hmc6301.direct_reg_access)
print("bb_attn1", hmc6301.bb_attn1)
print("bb_attn2", hmc6301.bb_attn2)
print("bb_attnq_fine", hmc6301.bb_attnq_fine)
print("bb_attni_fine", hmc6301.bb_attni_fine)
print("bb_lpc", hmc6301.bb_lpc)
print("bb_lpc", hmc6301.bb_hpc)
#Channel attribute:
print("raw_value", hmc6301.channel["temp"].raw)