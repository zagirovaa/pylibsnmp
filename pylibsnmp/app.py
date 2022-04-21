#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from device import Device


dev = Device()
dev.name = "Cisco 3750"
dev.community = "iMAXPublic"
dev.address = "192.168.10.42"
if dev.connect():
    print(dev.get_if_out_bandwidth(dev.indexes[0]))
