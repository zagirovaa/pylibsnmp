#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from pylibsnmp import device


dev = device.Device()
dev.community = "public"
dev.address = "192.168.7.1"
dev.version = 2
if dev.connect():
    print(dev)
