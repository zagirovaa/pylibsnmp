#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from device import Device


dev = Device()
dev.community = "public"
dev.address = "192.168.10.206"
dev.version = 2
if dev.connect():
    for i in dev.indexes:
        print("Port " + str(i) + " is in " + dev.get_if_admin_status(i) + " state.")
