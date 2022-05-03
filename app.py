#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from pylibsnmp.device import NetDevice


snmp_settings = ("public", "192.168.10.206", 2)
device = NetDevice()
device.community, device.address, device.version = snmp_settings
if device.connect():
    print(device.get_if_mtu(device.indexes[0]))
