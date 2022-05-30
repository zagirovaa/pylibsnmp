#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from pylibsnmp import helpers


class TestHelpers:
    def test_get_bits(self):
        result = helpers.get_bits(8)
        assert result == 64

    def test_get_mac_from_octets(self):
        result = helpers.get_mac_from_octets("ÔÊmhçn")
        assert not result == "AA:BB:CC:DD:EE:FF"
        assert result == "D4:CA:6D:68:E7:6E"
        result = helpers.get_mac_from_octets("ÔÊmhçn", "-")
        assert result == "D4-CA-6D-68-E7-6E"
        result = helpers.get_mac_from_octets("ÔÊmhçn", ".")
        assert result == "D4CA.6D68.E76E"

    def test_get_speed(self):
        assert helpers.get_speed(1073741824) == 1.0
        assert helpers.get_speed(12345678910) == 11.5
        assert helpers.get_speed(1048576) == 1.0
        assert helpers.get_speed(123456789) == 117.7
        assert helpers.get_speed(1024) == 1.0
        assert helpers.get_speed(123456) == 120.6
        assert helpers.get_speed(500) == 500

    def test_get_unit(self):
        assert helpers.get_unit(1073741824) == "Gbits/s"
        assert helpers.get_unit(1073742324) == "Gbits/s"
        assert helpers.get_unit(1048576) == "Mbits/s"
        assert helpers.get_unit(1049076) == "Mbits/s"
        assert helpers.get_unit(1024) == "Kbits/s"
        assert helpers.get_unit(1524) == "Kbits/s"
        assert helpers.get_unit(500) == "Bits/s"

    def test_is_ip_address(self):
        assert helpers.is_ip_address("0.0.0.0")
        assert helpers.is_ip_address("255.255.255.255")
        assert helpers.is_ip_address("192.168.0.255")
        assert not helpers.is_ip_address("192.168.0.256")
