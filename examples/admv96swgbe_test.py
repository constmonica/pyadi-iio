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
admv96swgbe = adi.admv96swgbe(uri="serial:/dev/ttyACM0,115200,8n2n")

# Device-specific attributes
admv96swgbe.tx_autotuning = True
print("Tx autotuning: ", admv96swgbe.tx_autotuning)
admv96swgbe.tx_target = 357
print("Tx target: ", admv96swgbe.tx_target)
print("Tx tolerance: ", admv96swgbe.tx_tolerance)
admv96swgbe.rx_autotuning = True
print("Rx autotuning: ", admv96swgbe.rx_autotuning)
admv96swgbe.rx_target = 1952
print("Rx target: ", admv96swgbe.rx_target)
print("Rx tolerance: ", admv96swgbe.rx_tolerance)
print("Tx auto ifvga: ", admv96swgbe.tx_auto_ifvga)
print("Rx auto ifvga_rflna: ", admv96swgbe.rx_auto_ifvga_rflna)
print("Reset: ", admv96swgbe.reset)

# Channel attributes 
print("Tx det scale:", admv96swgbe.channel["voltage0"].scale)
print("Tx det raw:", admv96swgbe.channel["voltage0"].raw)
print("Rx det scale:", admv96swgbe.channel["voltage1"].scale)
print("Rx det raw:", admv96swgbe.channel["voltage1"].raw)
