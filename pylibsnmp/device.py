#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from __future__ import annotations
from typing import Dict, Tuple, List
import logging

from easysnmp import Session

import snmp
from helpers import is_ip_address


class Device:
    """
    Class for creating snmp enabled network devices
    """

    # Interface speed coefficient
    # For 10 Mb/s speed we get value of 10000000
    # speed x 1000000
    COEFFICIENT: int = 1000000
    # Supported SNMP versions
    VERSIONS: Tuple[int] = (1, 2)

    # Number of devices counter
    dev_number = 0
    # SNMP default parameters
    default: Dict[str, any] = {
        "name": "device",
        "address": "127.0.0.1",
        "port": 161,
        "community": "public",
        "version": 2
    }

    def __init__(
            self,
            name: str = default["name"],
            address: str = default["address"],
            port: int = default["port"],
            community: str = default["community"],
            version: int = default["version"]) -> None:
        """ Constructor """

        # Incrementing device number counter each time object is created
        Device.dev_number += 1
        # Device name must be wet or will be given a default name
        if not name.strip() or name == Device.default["name"]:
            name = Device.default["name"] + str(Device.dev_number)
        self.__name: str = name
        # Ip address must be set and have an appropriate format
        if not address or not is_ip_address(address):
            address = Device.default["address"]
        self.__address: str = address
        # Port must be set and have value between 1 and 65535
        if 1 > port > 65535:
            port = Device.default["port"]
        self.__port: int = port
        # Community must be set
        if not community.strip():
            community = Device.default["community"]
        self.__community: str = community
        # Version must be set and be one of supported
        if version not in Device.VERSIONS:
            version = Device.default["version"]
        self.__version: int = version
        self.__session: Session = None
        self.__description: str = ""
        self.__uptime: str = ""
        self.__contact: str = ""
        self.__location: str = ""
        self.__count: int = 0
        self.__indexes: List[int] = []
        self.__autoupdate: bool = False

    def __str__(self) -> str:
        """
        Returns information about object in human readable format
        """

        value: str = (
            "Name:          {0}\n"
            "Address:       {1}\n"
            "Port:          {2}\n"
            "Community:     {3}\n"
            "Version:       {4}\n"
        )
        return value.format(
            self.__name,
            self.__address,
            str(self.__port),
            self.__community,
            str(self.__version)
        )

    # ---------------------------------------
    # Setters and getters declaration section
    # ---------------------------------------
    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, new_value: str) -> None:
        if type(new_value) == str:
            new_value.strip()
            if new_value:
                self.__name = new_value
            else:
                logging.error("Value is empty.")
        else:
            logging.error("Value format is incorrect.")

    @property
    def address(self) -> str:
        return self.__address

    @address.setter
    def address(self, new_value: str) -> None:
        if type(new_value) == str:
            new_value.strip()
            if new_value and is_ip_address(new_value):
                self.__address = new_value
            else:
                logging.error(
                    "IP address is empty or has an incorrect format."
                )
        else:
            logging.error("IP address has to be in text string format.")

    @property
    def port(self) -> int:
        return self.__port

    @port.setter
    def port(self, new_value: int) -> None:
        if 1 > new_value > 65535:
            self.__version = new_value
        else:
            logging.error("Port number is out of range.")

    @property
    def community(self) -> str:
        return self.__community

    @community.setter
    def community(self, new_value: str) -> None:
        if type(new_value) == str:
            new_value.strip()
            if new_value:
                self.__community = new_value
            else:
                logging.error("Community is not set.")
        else:
            logging.error("Community has to be in text string format.")

    @property
    def version(self) -> int:
        return self.__version

    @version.setter
    def version(self, new_value: int) -> None:
        if new_value in Device.VERSIONS:
            self.__version = new_value
        else:
            logging.error("Incorrect format or unsupported version of snmp.")

    @property
    def autoupdate(self) -> bool:
        return self.__autoupdate

    @autoupdate.setter
    def autoupdate(self, new_value: bool) -> None:
        self.__autoupdate = new_value

    @property
    def description(self) -> str:
        return self.__description

    @property
    def uptime(self) -> str:
        return self.__uptime

    @property
    def contact(self) -> str:
        return self.__contact

    @property
    def location(self) -> str:
        return self.__location

    @property
    def count(self) -> int:
        return self.__count

    @property
    def indexes(self) -> List[int]:
        return self.__indexes

    # ----------------------------------
    # Public methods declaration section
    # ----------------------------------
    def connect(self) -> bool:
        """
        Initiates connection
        """

        try:
            self.__session = Session(
                hostname=self.__address,
                remote_port=self.__port,
                community=self.__community,
                version=self.__version
            )
            self.populate()
            return True
        except Exception as err:
            logging.error("Could not connect to device.")
            logging.error(err)
        return False

    def disconnect(self) -> bool:
        """
        Drops connection
        """

        pass

    def reconnect(self) -> bool:
        """
        Drops connection and than initiates it again
        """

        self.disconnect()
        self.connect()

    def populate(self) -> None:
        """
        Populates device fields with necessary data
        """

        self.__description = self.__get_description()
        self.__count = self.__get_if_count()
        self.__indexes = self.__get_if_indexes()

    def get_if_type(self, port: int) -> int:
        """ Returns type of the given interface """

        port_type: int = 0
        if self.__count > 0 and port in self.__indexes:
            try:
                snmp_data = self.__session.get(
                    snmp.OIDS["IF_TYPE"] + str(port)
                )
            except Exception as err:
                logging.error("Could not get interface type.")
                logging.error(err)
            else:
                interface_value = snmp_data.value
                if interface_value.isdigit():
                    port_type = int(interface_value)
                else:
                    logging.error(
                        "Interface type has to be in digital format."
                    )
        else:
            logging.error(
                "No interface or given interface number is incorrect."
            )
        return port_type

    def get_if_speed(self, port: int) -> int:
        """ Returns speed of the given interface """

        port_speed: int = 0
        if self.__count > 0 and port in self.__indexes:
            try:
                snmp_data = self.__session.get(
                    snmp.OIDS["IF_SPEED"] + str(port)
                )
            except Exception as err:
                logging.error("Could not get interface speed.")
                logging.error(err)
            else:
                interface_value = snmp_data.value
                if interface_value.isdigit():
                    interface_value = int(interface_value)
                    if interface_value > Device.COEFFICIENT:
                        port_speed = interface_value / Device.COEFFICIENT
                else:
                    logging.error(
                        "Interface number has to be in digital format."
                    )
        else:
            logging.error(
                "No interface or given interface number is incorrect."
            )
        return port_speed

    def get_if_in_bandwidth(self, port: int) -> int:
        """ Returns number of inboud packets on the given interface """

        port_bandwidth: int = 0
        if self.__count > 0 and port in self.__indexes:
            try:
                snmp_data = self.__session.get(
                    snmp.OIDS["IF_IN_OCTETS"] + str(port)
                )
            except Exception as err:
                logging.error("Could not get number of inboud bytes.")
                logging.error(err)
            else:
                interface_value = snmp_data.value
                if interface_value.isdigit():
                    port_bandwidth = int(interface_value)
                else:
                    logging.error(
                        "Number of inbound bytes has to be in digital format."
                    )
        else:
            logging.error(
                "No interface or given interface number is incorrect."
            )
        return port_bandwidth

    def get_if_out_bandwidth(self, port: int) -> int:
        """ Returns number of outbound bytes on the given interface """

        port_bandwidth: int = 0
        if self.__count > 0 and port in self.__indexes:
            try:
                snmp_data = self.__session.get(
                    snmp.OIDS["IF_OUT_OCTETS"] + str(port)
                )
            except Exception as err:
                logging.error("Could not get number of outboud bytes.")
                logging.error(err)
            else:
                interface_value = snmp_data.value
                if interface_value.isdigit():
                    port_bandwidth = int(interface_value)
                else:
                    logging.error(
                        "Number of outbound bytes has to be in digital format."
                    )
        else:
            logging.error(
                "No interface or given interface number is incorrect."
            )
        return port_bandwidth

    # -----------------------------------
    # Рrivate methods declaration section
    # -----------------------------------
    def __get_description(self) -> str:
        """
        Returns device description
        """

        description: str = ""
        try:
            snmp_data = self.__session.get(
                snmp.OIDS["SYS_DECRIPTION"]
            )
        except Exception as err:
            logging.error("Could not get device description.")
            logging.error(err)
        else:
            description = snmp_data.value
        return description

    def __get_if_count(self) -> int:
        """
        Returns number of interfaces
        """

        if_count: int = 0
        try:
            snmp_data = self.__session.get(snmp.OIDS["IF_NUMBER"])
        except Exception as err:
            logging.error("Could not get number of interfaces.")
            logging.error(err)
        else:
            data = snmp_data.value
            if data.isdigit():
                if_count = int(data)
            else:
                logging.error("Value format is incorrect.")
        return if_count

    def __get_if_indexes(self) -> List[int]:
        """
        Returns list of interfaces indexes
        """

        if_index: List[int] = []
        try:
            interfaces = self.__session.walk(snmp.OIDS["IF_INDEX"])
        except Exception as err:
            logging.error("Could not get list of interface indexes.")
            logging.error(err)
        else:
            index_count: int = len(interfaces)
            if index_count > 0:
                for interface in interfaces:
                    if_index.append(int(interface.value))
            else:
                logging.error("No interface index found.")
        return if_index
