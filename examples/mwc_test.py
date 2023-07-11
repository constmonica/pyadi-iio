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


# Set up MWC device
mwc = adi.mwc(uri="serial:/dev/ttyACM0,115200,8n2n")

# Device-specific attributes
mwc.tx_autotuning = True
print("Tx autotuning: ", mwc.tx_autotuning)
mwc.tx_target = 357
print("Tx target: ", mwc.tx_target)
print("Tx tolerance: ", mwc.tx_tolerance)
mwc.rx_autotuning = True
print("Rx autotuning: ", mwc.rx_autotuning)
mwc.rx_target = 1952
print("Rx target: ", mwc.rx_target)
print("Rx tolerance: ", mwc.rx_tolerance)
print("Tx auto ifvga: ", mwc.tx_auto_ifvga)
print("Rx auto ifvga_rflna: ", mwc.rx_auto_ifvga_rflna)
print("Reset: ", mwc.reset)
print("save_defaults: ", mwc.save_defaults)
print("hw_version", mwc.hw_version)
print("carrier_version", mwc.carrier_version)
print("save value: ", mwc.save)
print("hw_version:", mwc.hw_version)
print("carrier version:", mwc.carrier_version)
print("Carrier serial:", mwc.hw_serial)

# Channel attributes 
print("Tx det scale:", mwc.channel["voltage0"].scale)
print("Tx det raw:", mwc.channel["voltage0"].raw)
print("Rx det scale:", mwc.channel["voltage1"].scale)
print("Rx det raw:", mwc.channel["voltage1"].raw)
