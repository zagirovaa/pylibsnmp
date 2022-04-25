#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from math import floor
from time import sleep

from pylibsnmp import device


def get_bits(octets: int) -> int:
    # An octet is really just a fancy name for a "byte".
    # So if you multiply this number by 8 you get bits.
    return octets * 8


def get_speed(bits: int) -> int:
    if bits > 1024 * 1024 * 1024:
        speed = floor((bits / (1024 * 1024 * 1024)))
    elif bits > 1024 * 1024:
        speed = floor(bits / (1024 * 1024))
    elif bits > 1024:
        speed = floor(bits / 1024)
    else:
        speed = bits
    return speed


def get_unit(bits: int) -> str:
    if bits > 1024 * 1024 * 1024:
        unit = "Gbits/s"
    elif bits > 1024 * 1024:
        unit = "Mbits/s"
    elif bits > 1024:
        unit = "Kbits/s"
    else:
        unit = "Bits/s"
    return unit


dev = device.Device()
dev.community = "public"
dev.address = "192.168.10.206"
dev.version = 2
if dev.connect():
    prev_rx = dev.get_if_in_bandwidth(1)
    prev_tx = dev.get_if_out_bandwidth(1)
    sleep(1)
    for i in range(100):
        curr_rx = dev.get_if_in_bandwidth(1)
        curr_tx = dev.get_if_out_bandwidth(1)
        in_speed = get_speed(get_bits(curr_rx) - get_bits(prev_rx))
        out_speed = get_speed(get_bits(curr_tx) - get_bits(prev_tx))
        in_unit = get_unit(get_bits(curr_rx) - get_bits(prev_rx))
        out_unit = get_unit(get_bits(curr_tx) - get_bits(prev_tx))
        prev_rx = curr_rx
        prev_tx = curr_tx
        print("In: {} {} Out: {} {}".format(
            in_speed, in_unit, out_speed, out_unit
        ))
        sleep(1)
