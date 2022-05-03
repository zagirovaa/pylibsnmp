#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from pylibsnmp import device


dev = device.Device()
dev.community = "iMAXPublic"
dev.address = "192.168.12.25"
dev.version = 2
if dev.connect():
    print(dev.iftypes)
