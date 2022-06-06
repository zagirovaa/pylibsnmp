#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
Python module with helper functions used in the project.

- class SetInterval()

- def get_bits(octets: int) -> int:

- def get_bits(octets: int) -> int:

- def get_mac_from_octets(octets: str, delimiter: str = ":") -> str:

- def get_speed(bits: int) -> int:

- def get_unit(bits: int) -> str:

- def is_ip_address(address: str) -> bool:

- def is_port_number(port: int) -> bool:
"""


from __future__ import annotations
from threading import Timer


class SetInterval():
    """
    Class for creating python alternative to
    JavaScript setInterval function
    """

    def __init__(self, func, sec: int) -> None:
        def func_wrapper() -> None:
            self.thread = Timer(sec, func_wrapper)
            self.thread.start()
            func()
        self.thread = Timer(sec, func_wrapper)
        self.thread.start()

    def cancel(self):
        self.thread.cancel()


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
    Converts bits to Gbits/s, Mbits/s, Kbits/s
    """

    if bits >= 1024 * 1024 * 1024:
        speed = round(bits / (1024 * 1024 * 1024), 1)
    elif bits >= 1024 * 1024:
        speed = round(bits / (1024 * 1024), 1)
    elif bits >= 1024:
        speed = round(bits / 1024, 1)
    else:
        speed = bits
    return speed


def get_unit(bits: int) -> str:
    """
    Returns unit type according to bits count
    """

    if bits >= 1024 * 1024 * 1024:
        unit = "Gbits/s"
    elif bits >= 1024 * 1024:
        unit = "Mbits/s"
    elif bits >= 1024:
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
            if (
                not result[octet].isdigit or
                int(result[octet]) > 255 or
                int(result[octet]) < 0
            ):
                return False
        return True


def is_port_number(port: int) -> bool:
    """
    Function checks whether port number
    argument has an appropriate value
    """
    if type(port) is int:
        if port > 0 and port <= 65535:
            return True
