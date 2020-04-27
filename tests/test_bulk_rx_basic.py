#!/usr/bin/env python
# Copyright (c) 2016-2020, XMOS Ltd, All rights reserved

import random
import xmostest
from  usb_packet import *
import usb_packet
from usb_clock import Clock
from helpers import do_usb_test, runall_rx

def do_test(arch, clk, phy, seed):
    rand = random.Random()
    rand.seed(seed)

    ep = 1
    address = 1

    # The inter-frame gap is to give the DUT time to print its output
    packets = []

    dataval = 0;

    pid = PID_DATA0;

    for pktlength in range(10, 20):

        AppendOutToken(packets, ep, address, inter_pkt_gap=500)
        packets.append(TxDataPacket(rand, data_start_val=dataval, length=pktlength, pid=pid)) 
        packets.append(RxHandshakePacket())
   
        if(pid == usb_packet.PID_DATA1):
            pid = usb_packet.PID_DATA0;
        else:
            pid = usb_packet.PID_DATA1;

        dataval += pktlength

    do_usb_test(arch, clk, phy, packets, __file__, seed, level='smoke', extra_tasks=[])

def runtest():
    random.seed(1)
    runall_rx(do_test)
