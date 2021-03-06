# Copyright (c) 2015-2019, XMOS Ltd, All rights reserved

import usb.core
import usb.util

# Find XMOS USBTMC test device
dev = usb.core.find(idVendor=0x20b1, idProduct=0x2337)


import usbtmc
instr =  usbtmc.Instrument(0x20b1, 0x2337)

# Test SCPI commands
# ------------------

print('Starting basic SCPI commands testing...')
print ('')

# Request device identification details
print(instr.ask("*IDN?"))

# Reset device; this command is not implemented!
print(instr.ask("*RST"))
print ('')

# Fetch DC voltage value from the device
print(instr.ask("*MEASure:VOLTage:DC?"))


print('Exiting...')
