#!/usr/bin/env python
# Copyright (c) 2016-2019, XMOS Ltd, All rights reserved

#Generate a SETUP transaction that is too short... with a bad CRC
#Dont really expect a short packet with a good CRC - would be a very bad host (though would be good to be able to handle this..)

import random
import xmostest
from usb_packet import AppendSetupToken, TxDataPacket, RxDataPacket, TokenPacket, RxHandshakePacket, TxHandshakePacket
from usb_clock import Clock
from helpers import do_rx_test, packet_processing_time, get_dut_address
from helpers import choose_small_frame_size, check_received_packet, runall_rx


# Single, setup transaction to EP 0

def do_test(arch, tx_clk, tx_phy, seed):
    rand = random.Random()
    rand.seed(seed)

    dev_address = get_dut_address()
    ep = 0

    # The inter-frame gap is to give the DUT time to print its output
    packets = []

    AppendSetupToken(packets, ep)
    packets.append(TxDataPacket(rand, length=3, pid=3, bad_crc=True))
    #packets.append(RxHandshakePacket())

    AppendSetupToken(packets, ep)
    packets.append(TxDataPacket(rand, length=8, pid=3, bad_crc=False))
    packets.append(RxHandshakePacket(timeout=11))

    # Note, quite big gap to allow checking.

    packets.append(TokenPacket( 
        inter_pkt_gap=2000, 
        pid=0xe1, #OUT
        address=dev_address, 
        endpoint=ep))

    packets.append(TxDataPacket(rand, length=10, pid=0xb))
    
    packets.append(RxHandshakePacket())

    packets.append(TokenPacket( 
        inter_pkt_gap=2000, 
        pid=0x69, #OUT
        address=dev_address, 
        endpoint=ep))
   
    #Expect 0-length
    packets.append(RxDataPacket(rand, length=0, pid=0x4b))

    # Send ACK
    packets.append(TxHandshakePacket())

    do_rx_test(arch, tx_clk, tx_phy, packets, __file__, seed,
               level='smoke', extra_tasks=[])

def runtest():
    random.seed(1)
    runall_rx(do_test)
