#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from pylibsnmp.device import NetDevice


snmp_settings = ("192.168.10.206")
device = NetDevice()
device.address, device.community, device.version = snmp_settings
if device.connect():
    print(device)
