#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from pylibsnmp.device import NetDevice


device = NetDevice(address="192.168.10.206")
if device.connect():
    print(device)
