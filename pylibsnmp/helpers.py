#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
Python module with helper functions used in the project.
"""


from __future__ import annotations
from typing import Callable
from threading import Timer


class SetInterval():
    """
    Class for creating python alternative to JavaScript setInterval function.
    """

    def __init__(self, func: Callable, sec: int) -> None:
        """
        Class constructor.

        params:
            | func: {Callable} - function to execute
            | sec: {int} - interval in seconds to execute func
        """

        def func_wrapper() -> None:
            self.thread = Timer(sec, func_wrapper)
            self.thread.start()
            func()
        self.thread = Timer(sec, func_wrapper)
        self.thread.start()

    def cancel(self):
        """
        Cancels Timer object in order for the application to end correctly.
        """

        self.thread.cancel()


def get_bits(octets: int) -> int:
    """
    Converts octets to bits.

    An octet is really just a fancy name for a "byte".
    So if you multiply this number by 8 you get bits.
    """

    return octets * 8


def get_mac_from_octets(octets: str, delimiter: str = ":") -> str:
    """
    Converts octets to mac address.

    When requesting physical address of the device
    using snmp responce comes in the format of octets.

    In order to convert it to mac address:
    | - get list of ascii codes of octets
    | - convert it to bytearray
    | - convert it to hex format
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
    Converts bits to Kbits/s, Mbits/s or Gbits/s according to the bits count.
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
    Returns unit type according to the bits count.
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
    Checks the string to be in ip address format.

    IP address have to:
    | - have four octets
    | - each octet must be from 0 to 255
    | - each octet must be in digital format
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
    Checks whether port number argument has an appropriate value.

    Port number has to be in the range of 1 and 65535.
    """

    if type(port) is int:
        if port > 0 and port <= 65535:
            return True
