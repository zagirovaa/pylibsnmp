#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from __future__ import annotations
from typing import List


def is_ip_address(address: str) -> bool:
    """
    Checks the string to be in ip address format
    """

    result: List[str] = address.strip().split(".")
    if len(result) == 4:
        for octet in range(0, 4):
            if not result[octet].isdigit or 0 > int(result[octet]) > 255:
                return False
        return True
    return False


def get_mac_from_octets(octets: str, delimiter: str = ":") -> str:
    """
    Converts octets to mac address
    """

    step: int = 2
    if delimiter == ".":
        step = 4
    list_of_bytes: List[int] = [ord(octet) for octet in list(octets)]
    # Mac address in the format of AABBCCDDEEFF
    mac_address: str = bytearray(list_of_bytes).hex().upper()
    # Converts AABBCCDDEEFF to AA:BB:CC:DD:EE:FF
    result: str = delimiter.join(
        # Mac address consists of 12 symbols (0..9, a..f, A..F)
        [mac_address[i:i+step] for i in range(0, 12, step)]
    )
    return result
