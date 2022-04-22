#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from __future__ import annotations
from typing import Dict


OIDS: Dict[str, str] = {
    "SYS_DECRIPTION":       "1.3.6.1.2.1.1.1.0",
    "SYS_UPTIME":           "1.3.6.1.2.1.1.3.0",
    "SYS_CONTACT":          "1.3.6.1.2.1.1.4.0",
    "SYS_NAME":             "1.3.6.1.2.1.1.5.0",
    "SYS_LOCATION":         "1.3.6.1.2.1.1.6.0",
    "IF_NUMBER":            "1.3.6.1.2.1.2.1.0",
    "IF_INDEX":             "1.3.6.1.2.1.2.2.1.1.",
    "IF_DESCRIPTION":       "1.3.6.1.2.1.2.2.1.2.",
    "IF_TYPE":              "1.3.6.1.2.1.2.2.1.3.",
    "IF_SPEED":             "1.3.6.1.2.1.2.2.1.5.",
    "IF_ADMIN_STATUS":      "1.3.6.1.2.1.2.2.1.7.",
    "IF_OPER_STATUS":       "1.3.6.1.2.1.2.2.1.8.",
    "IF_LAST_CHANGE":       "1.3.6.1.2.1.2.2.1.9.",
    "IF_IN_OCTETS":         "1.3.6.1.2.1.2.2.1.10.",
    "IF_IN_UNICAST":        "1.3.6.1.2.1.2.2.1.11.",
    "IF_IN_DISCARDS":       "1.3.6.1.2.1.2.2.1.13.",
    "IF_IN_ERRORS":         "1.3.6.1.2.1.2.2.1.14.",
    "IF_OUT_OCTETS":        "1.3.6.1.2.1.2.2.1.16.",
    "IF_OUT_UNICAST":       "1.3.6.1.2.1.2.2.1.17.",
    "IF_OUT_DISCARDS":      "1.3.6.1.2.1.2.2.1.19.",
    "IF_OUT_ERRORS":        "1.3.6.1.2.1.2.2.1.20.",
    "IF_IN_MULTICAST":      "1.3.6.1.2.1.31.1.1.1.2.",
    "IF_IN_BROADCAST":      "1.3.6.1.2.1.31.1.1.1.3.",
    "IF_OUT_MULTICAST":     "1.3.6.1.2.1.31.1.1.1.4.",
    "IF_OUT_BROADCAST":     "1.3.6.1.2.1.31.1.1.1.5.",
    "IF_HIGH_SPEED":        "1.3.6.1.2.1.31.1.1.1.15."
}

IF_TYPES: Dict[str, str] = {
    "1":    "other",
    "2":    "regular1822",
    "3":    "hdh1822",
    "4":    "ddn-x25",
    "5":    "rfc877-x25",
    "6":    "ethernet-csmacd",
    "7":    "iso88023-csmacd",
    "8":    "iso88024-tokenBus",
    "9":    "iso88025-tokenRing",
    "10":   "iso88026-man",
    "11":   "starLan",
    "12":   "proteon-10Mbit",
    "13":   "proteon-80Mbit",
    "14":   "hyperchannel",
    "15":   "fddi",
    "16":   "lapb",
    "17":   "sdlc",
    "18":   "ds1",
    "19":   "e1",
    "20":   "basicISDN",
    "21":   "primaryISDN",
    "22":   "propPointToPointSerial",
    "23":   "ppp",
    "24":   "softwareLoopback",
    "25":   "eon",
    "26":   "ethernet-3Mbit",
    "27":   "nsip",
    "28":   "slip",
    "29":   "ultra",
    "30":   "ds3",
    "31":   "sip",
    "32":   "frame-relay"
}
