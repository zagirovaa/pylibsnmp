#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from __future__ import annotations
from math import floor


def get_bits(octets: int) -> int:
    """
    Converts octets to bits
    """

    # An octet is really just a fancy name for a "byte".
    # So if you multiply this number by 8 you get bits.
    return octets * 8


def get_mac_from_octets(octets: str, delimiter: str = ":") -> str:
    """
    Converts octets to mac address
    """

    step = 2
    if delimiter == ".":
        step = 4
    list_of_bytes = [ord(octet) for octet in list(octets)]
    # Mac address in the format of AABBCCDDEEFF
    mac_address = bytearray(list_of_bytes).hex().upper()
    # Converts AABBCCDDEEFF to AA:BB:CC:DD:EE:FF
    result = delimiter.join(
        # Mac address consists of 12 symbols (0..9, a..f, A..F)
        [mac_address[i:i+step] for i in range(0, 12, step)]
    )
    return result


def get_speed(bits: int) -> int:
    """
    Converts bits to bits/s
    Gbits/s, Mbits/s, Kbits/s or Bits/s
    """

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
    """
    Returns unit type according to bits count
    """

    if bits > 1024 * 1024 * 1024:
        unit = "Gbits/s"
    elif bits > 1024 * 1024:
        unit = "Mbits/s"
    elif bits > 1024:
        unit = "Kbits/s"
    else:
        unit = "Bits/s"
    return unit


def is_ip_address(address: str) -> bool:
    """
    Checks the string to be in ip address format
    """

    result = address.strip().split(".")
    if len(result) == 4:
        for octet in range(0, 4):
            if not result[octet].isdigit or 0 > int(result[octet]) > 255:
                return False
        return True
    return False
