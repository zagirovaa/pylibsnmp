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
