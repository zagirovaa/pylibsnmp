#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from time import sleep

from .pylibsnmp.device import NetDevice


snmp_settings = ("192.168.10.206", "public", 2)
device = NetDevice()
device.address, device.community, device.version = snmp_settings
if device.connect():
    print(device)
    device.updatetime = 5
    device.autoupdate = True
    sleep(5)
    print(device)
    device.disconnect()
