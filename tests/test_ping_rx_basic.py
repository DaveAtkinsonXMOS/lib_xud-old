#!/usr/bin/env python
# Copyright (c) 2016-2019, XMOS Ltd, All rights reserved

# Basic check of PING functionality

import random
import xmostest
from  usb_packet import *
from usb_clock import Clock
from helpers import do_usb_test, runall_rx

def do_test(arch, clk, phy, seed):
    rand = random.Random()
    rand.seed(seed)

    address = 1
    ep = 1

    # The inter-frame gap is to give the DUT time to print its output
    packets = []

    dataval = 0;

    # Ping EP 2, expect NAK
    AppendPingToken(packets, 2, address)
    packets.append(RxHandshakePacket(pid=0x5a))

    # And again
    AppendPingToken(packets, 2, address)
    packets.append(RxHandshakePacket(pid=0x5a))

    # Send packet to EP 1, xCORE should mark EP 2 as ready
    AppendOutToken(packets, ep, address)
    packets.append(TxDataPacket(rand, data_start_val=dataval, length=10, pid=0x3)) #DATA0
    packets.append(RxHandshakePacket())
    
    # Ping EP 2 again - expect ACK
    AppendPingToken(packets, 2, address, inter_pkt_gap=6000)
    packets.append(RxHandshakePacket())

    # And again..
    AppendPingToken(packets, 2, address)
    packets.append(RxHandshakePacket())

    # Send out to EP 2.. expect ack
    AppendOutToken(packets, 2,address,  inter_pkt_gap=6000)
    packets.append(TxDataPacket(rand, data_start_val=dataval, length=10, pid=0x3)) #DATA0
    packets.append(RxHandshakePacket())

    # Re-Ping EP 2, expect NAK
    AppendPingToken(packets, 2, address)
    packets.append(RxHandshakePacket(pid=0x5a))

    # And again
    AppendPingToken(packets, 2, address)
    packets.append(RxHandshakePacket(pid=0x5a))

    # Send a packet to EP 1 so the DUT knows it can exit.
    AppendOutToken(packets, ep, address)
    packets.append(TxDataPacket(rand, data_start_val=dataval+10, length=10, pid=0x3^8)) #DATA1
    packets.append(RxHandshakePacket())

    do_usb_test(arch, clk, phy, packets, __file__, seed,level='smoke', extra_tasks=[])

def runtest():
    random.seed(1)
    runall_rx(do_test)
