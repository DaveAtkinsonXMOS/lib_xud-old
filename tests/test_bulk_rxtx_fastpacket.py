#!/usr/bin/env python
# Copyright (c) 2016-2019, XMOS Ltd, All rights reserved

import random
import xmostest
from  usb_packet import *
from usb_clock import Clock
from helpers import do_rx_test, packet_processing_time, get_dut_address
from helpers import choose_small_frame_size, check_received_packet, runall_rx

def do_test(arch, clk, phy, seed):
    rand = random.Random()
    rand.seed(seed)

    ep = 3

    packets = []

    data_val = 0;
    pkt_length = 20
    data_pid = 0x3 #DATA0 

    for pkt_length in range(10, 20):

        # < 17 fails for SI
        # < 37 fails for DI
        AppendOutToken(packets, ep, inter_pkt_gap=37)
        packets.append(TxDataPacket(rand, data_start_val=data_val, length=pkt_length, pid=data_pid)) #DATA0
        # 9 works for SI
        packets.append(RxHandshakePacket(timeout=10))

        AppendInToken(packets, ep, inter_pkt_gap=0)
        packets.append(RxDataPacket(rand, data_start_val=data_val, length=pkt_length, pid=data_pid))
        packets.append(TxHandshakePacket())

        data_val = data_val + pkt_length
        data_pid = data_pid ^ 8

    do_rx_test(arch, clk, phy, packets, __file__, seed,
               level='smoke', extra_tasks=[])

def runtest():
    random.seed(1)
    runall_rx(do_test)
