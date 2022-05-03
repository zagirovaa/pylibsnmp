#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from __future__ import annotations
from datetime import timedelta
import logging
from typing import List

from easysnmp import Session

from pylibsnmp import snmp
from pylibsnmp import helpers


class NetDevice:
    """
    Class for creating snmp enabled network devices
    """

    # Interface speed coefficient
    # For 10 Mb/s speed we get value of 10000000
    # speed x 1000000
    COEFFICIENT = 1000000
    # Supported SNMP versions
    VERSIONS = (1, 2)
    # SNMP default parameters
    DEFAULT = {
        "ADDRESS": "127.0.0.1",
        "PORT": 161,
        "COMMUNITY": "public",
        "VERSION": 2
    }
    # Delimiters allowed in mac address
    DELIMITERS = (":", "-", ".")

    def __init__(
            self,
            address=DEFAULT["ADDRESS"],
            port=DEFAULT["PORT"],
            community=DEFAULT["COMMUNITY"],
            version=DEFAULT["VERSION"]) -> None:
        """
        Constructor
        """

        # Ip address must be set and have an appropriate format
        if not address.strip() or not helpers.is_ip_address(address):
            address = NetDevice.DEFAULT["ADDRESS"]
        self.__address = address
        # Community must be set
        if not community.strip():
            community = NetDevice.DEFAULT["COMMUNITY"]
        self.__community = community
        # Port must be set and have value between 1 and 65535
        if 1 > port > 65535:
            port = NetDevice.DEFAULT["PORT"]
        self.__port = port
        # Version must be set and be one of supported
        if version not in NetDevice.VERSIONS:
            version = NetDevice.DEFAULT["VERSION"]
        self.__version = version

        self.__autoupdate = False
        self.__contact = ""
        self.__count = 0
        self.__description = ""
        self.__types = []
        self.__indexes = []
        self.__location = ""
        self.__name = ""
        self.__session = None
        # Each 60 seconds count and indexes will be updated
        self.__updatetime = 60
        self.__uptime = ""

    def __str__(self) -> str:
        """
        Returns information about object in human readable format
        """

        value = (
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
    def address(self) -> str:
        return self.__address

    @address.setter
    def address(self, new_value) -> None:
        if type(new_value) == str:
            new_value.strip()
            if new_value and helpers.is_ip_address(new_value):
                self.__address = new_value
            else:
                logging.error(
                    "IP address is empty or has an incorrect format."
                )
        else:
            logging.error("IP address has to be in text string format.")

    @property
    def community(self) -> str:
        return self.__community

    @community.setter
    def community(self, new_value) -> None:
        if type(new_value) == str:
            new_value.strip()
            if new_value:
                self.__community = new_value
            else:
                logging.error("Community is not set.")
        else:
            logging.error("Community has to be in text string format.")

    @property
    def port(self) -> int:
        return self.__port

    @port.setter
    def port(self, new_value) -> None:
        if 1 > new_value > 65535:
            self.__version = new_value
        else:
            logging.error("Port number is out of range.")

    @property
    def version(self) -> int:
        return self.__version

    @version.setter
    def version(self, new_value) -> None:
        if new_value in NetDevice.VERSIONS:
            self.__version = new_value
        else:
            logging.error("Incorrect format or unsupported version of snmp.")

    @property
    def autoupdate(self) -> bool:
        return self.__autoupdate

    @autoupdate.setter
    def autoupdate(self, new_value) -> None:
        self.__autoupdate = new_value

    @property
    def count(self) -> int:
        return self.__count

    @property
    def contact(self) -> str:
        return self.__contact

    @property
    def description(self) -> str:
        return self.__description

    @property
    def indexes(self) -> List[int]:
        return self.__indexes

    @property
    def location(self) -> str:
        return self.__location

    @property
    def name(self) -> str:
        return self.__name

    @property
    def types(self) -> List[str]:
        return self.__types

    @property
    def updatetime(self) -> int:
        return self.__updatetime

    @updatetime.setter
    def updatetime(self, new_value) -> None:
        if type(new_value) == int:
            self.__updatetime = new_value
        else:
            logging.error("Incorrect format of update time.")

    @property
    def uptime(self) -> str:
        return self.__uptime

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
            self.__populate()
            return True
        except Exception as err:
            logging.error("Could not connect to device.")
            logging.error(err)
        return False

    def get_if_admin_status(self, port: int) -> str:
        """
        Returns admin status of the given interface
        """

        status: str = ""
        if self.__count > 0 and port in self.__indexes:
            try:
                snmp_data = self.__session.get(
                    snmp.OIDS["IF_ADMIN_STATUS"] + str(port)
                )
            except Exception as err:
                logging.error("Could not get interface admin status.")
                logging.error(err)
            else:
                value = snmp_data.value
                if value.isdigit():
                    status = snmp.IF_ADMIN_STATES[value]
                else:
                    logging.error(
                        "Interface admin status has to be in digital format."
                    )
        else:
            logging.error(
                "No interface or given interface number is incorrect."
            )
        return status

    def get_if_description(self, port: int) -> str:
        """
        Returns description of the given interface
        """

        description: str = ""
        if self.__count > 0 and port in self.__indexes:
            try:
                snmp_data = self.__session.get(
                    snmp.OIDS["IF_DESCRIPTION"] + str(port)
                )
            except Exception as err:
                logging.error("Could not get interface description.")
                logging.error(err)
            else:
                description = snmp_data.value
        else:
            logging.error(
                "No interface or given interface number is incorrect."
            )
        return description

    def get_if_in_bandwidth(self, port: int) -> int:
        """
        Returns number of inboud packets on the given interface
        """

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

    def get_if_last_change(self, port: int) -> str:
        """
        Returns when the given interface entered
        its operational state for the last time
        """

        last_change: str = ""
        if self.__count > 0 and port in self.__indexes:
            try:
                snmp_data = self.__session.get(
                    snmp.OIDS["IF_LAST_CHANGE"] + str(port)
                )
            except Exception as err:
                logging.error(
                    "Could not get last change time of port number {}.".format(
                        str(port)
                    )
                )
                logging.error(err)
            else:
                value = snmp_data.value
                if value.isdigit():
                    last_change = str(timedelta(seconds=(int(value)) / 100))
                else:
                    logging.error(
                        "Last change time has to be in digital format."
                    )
        else:
            logging.error(
                "No interface or given interface number is incorrect."
            )
        return last_change

    def get_if_mtu(self, port: int) -> int:
        """
        Returns mtu value of the given interface
        """

        mtu: int = 0
        if self.__count > 0 and port in self.__indexes:
            try:
                snmp_data = self.__session.get(
                    snmp.OIDS["IF_MTU"] + str(port)
                )
            except Exception as err:
                logging.error(
                    "Could not get mtu value of port number {}.".format(
                        str(port)
                    )
                )
                logging.error(err)
            else:
                value = snmp_data.value
                if value.isdigit():
                    mtu = int(value)
                else:
                    logging.error(
                        "Mtu value has to be in digital format."
                    )
        else:
            logging.error(
                "No interface or given interface number is incorrect."
            )
        return mtu

    def get_if_oper_status(self, port: int) -> str:
        """
        Returns operation status of the given interface
        """

        status: str = ""
        if self.__count > 0 and port in self.__indexes:
            try:
                snmp_data = self.__session.get(
                    snmp.OIDS["IF_OPER_STATUS"] + str(port)
                )
            except Exception as err:
                logging.error("Could not get interface operation status.")
                logging.error(err)
            else:
                value = snmp_data.value
                if value.isdigit():
                    status = snmp.IF_OPER_STATES[value]
                else:
                    logging.error(
                        "Interface operation status " +
                        "has to be in digital format."
                    )
        else:
            logging.error(
                "No interface or given interface number is incorrect."
            )
        return status

    def get_if_out_bandwidth(self, port: int) -> int:
        """
        Returns number of outbound bytes on the given interface
        """

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

    def get_if_phys_address(self, port: int, delimiter: str = ":") -> str:
        """
        Returns physical address of the given interface
        """

        phys_address: str = ""
        if self.__count > 0 and port in self.__indexes:
            if delimiter in NetDevice.DELIMITERS:
                try:
                    snmp_data = self.__session.get(
                        snmp.OIDS["IF_PHYS_ADDRESS"] + str(port)
                    )
                except Exception as err:
                    logging.error(
                        "Could not get physical address of the interface."
                    )
                    logging.error(err)
                else:
                    if snmp_data.value:
                        phys_address = helpers.get_mac_from_octets(
                            snmp_data.value, delimiter
                        )
                    else:
                        logging.error(
                            "Interface has no physical address."
                        )
            else:
                logging.error(
                    "Invalid delimiter for physical address."
                )
        else:
            logging.error(
                "No interface or given interface number is incorrect."
            )
        return phys_address

    def get_if_speed(self, port: int) -> int:
        """
        Returns speed of the given interface
        """

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
                    if interface_value > NetDevice.COEFFICIENT:
                        port_speed = interface_value / NetDevice.COEFFICIENT
                else:
                    logging.error(
                        "Interface number has to be in digital format."
                    )
        else:
            logging.error(
                "No interface or given interface number is incorrect."
            )
        return port_speed

    def get_if_type(self, port: int) -> str:
        """
        Returns type of the given interface
        """

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
                value = snmp_data.value
                if value.isdigit():
                    port_type = snmp.IF_TYPES[value]
                else:
                    logging.error(
                        "Interface type has to be in digital format."
                    )
        else:
            logging.error(
                "No interface or given interface number is incorrect."
            )
        return port_type

    # -----------------------------------
    # Рrivate methods declaration section
    # -----------------------------------
    def __populate(self) -> None:
        """
        Populates device fields with necessary data
        """

        self.__count = self.__get_if_count()
        self.__contact = self.__get_contact()
        self.__description = self.__get_description()
        self.__indexes = self.__get_if_indexes()
        self.__types = self.__get_if_types()
        self.__location = self.__get_location()
        self.__name = self.__get_name()
        self.__uptime = self.__get_uptime()

    def __get_contact(self) -> str:
        """
        Returns device contact
        """

        return self.__get_sys_data(
            "SYS_CONTACT",
            "Could not get device contact."
        )

    def __get_if_count(self) -> int:
        """
        Returns number of interfaces
        """

        result = ""
        value = self.__get_sys_data(
            "IF_NUMBER",
            "Could not get number of interfaces."
        )
        if value.isdigit():
            result = int(value)
        else:
            logging.error("Value format is incorrect.")
        return result

    def __get_description(self) -> str:
        """
        Returns device description
        """

        return self.__get_sys_data(
            "SYS_DECRIPTION",
            "Could not get device description."
        )

    def __get_if_indexes(self) -> List[int]:
        """
        Returns list of interfaces indexes
        """

        result = []
        try:
            interfaces = self.__session.walk(snmp.OIDS["IF_INDEX"])
        except Exception as err:
            logging.error("Could not get list of interface indexes.")
            logging.error(err)
        else:
            index_count: int = len(interfaces)
            if index_count > 0:
                for interface in interfaces:
                    result.append(int(interface.value))
            else:
                logging.error("No interface index found.")
        return result

    def __get_if_types(self) -> List[str]:
        """
        Returns list of interface types
        """

        result = []
        for index in self.__indexes:
            if_type = self.get_if_type(index)
            if if_type not in result:
                result.append(if_type)
        return result

    def __get_location(self) -> str:
        """
        Returns device location
        """

        return self.__get_sys_data(
            "SYS_LOCATION",
            "Could not get device location."
        )

    def __get_name(self) -> str:
        """
        Returns device name
        """

        return self.__get_sys_data(
            "SYS_NAME",
            "Could not get device name."
        )

    def __get_sys_data(self, snmp_oid, error_msg) -> any:
        result = ""
        try:
            snmp_data = self.__session.get(
                snmp.OIDS[snmp_oid]
            )
        except Exception as err:
            logging.error(error_msg)
            logging.error(err)
        else:
            result = snmp_data.value
        return result

    def __get_uptime(self) -> str:
        """
        Returns device uptime
        """

        result = ""
        value = self.__get_sys_data(
            "SYS_UPTIME",
            "Could not get device uptime."
        )
        # result is the time (in hundredths of a second) since the
        # network management portion of the system was last re-initialized
        result = str(timedelta(seconds=(int(value)) / 100))
        return result
