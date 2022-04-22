#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from device import Device


dev = Device()
dev.name = "Switch"
dev.community = "public"
dev.address = "192.168.10.206"
dev.version = 2
if dev.connect():
    print(dev)
    print(dev.get_if_in_bandwidth(dev.indexes[0]))
    print(dev.get_if_out_bandwidth(dev.indexes[0]))
