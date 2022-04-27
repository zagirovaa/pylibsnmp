#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from pylibsnmp import device


dev = device.Device()
dev.community = "public"
dev.address = "192.168.10.206"
dev.version = 2
if dev.connect():
    if_names = [dev.get_if_description(index) for index in dev.indexes]
    print(if_names)
