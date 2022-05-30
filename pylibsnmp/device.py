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
    __COEFFICIENT = 1000000
    # Supported SNMP versions
    __VERSIONS = (1, 2)
    # SNMP default parameters
    __DEFAULT = {
        "ADDRESS": "127.0.0.1",
        "COMMUNITY": "public",
        "PORT": 161,
        "VERSION": 2
    }
    # Delimiters allowed in mac address
    __DELIMITERS = (":", "-", ".")

    def __init__(
            self,
            address=__DEFAULT["ADDRESS"],
            community=__DEFAULT["COMMUNITY"],
            port=__DEFAULT["PORT"],
            version=__DEFAULT["VERSION"]) -> None:
        """
        Constructor
        """

        # Ip address must be set and have an appropriate format
        if not address.strip() or not helpers.is_ip_address(address):
            address = NetDevice.__DEFAULT["ADDRESS"]
        self.__address = address
        # Community must be set
        if not community.strip():
            community = NetDevice.__DEFAULT["COMMUNITY"]
        self.__community = community
        # Port must be set and have value between 1 and 65535
        if not helpers.is_port_number(port):
            port = NetDevice.__DEFAULT["PORT"]
        self.__port = port
        # Version must be set and be one of supported
        if version not in NetDevice.__VERSIONS:
            version = NetDevice.__DEFAULT["VERSION"]
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
        # Each 60 seconds device related data will be populated
        self.__updatetime = 60
        self.__uptime = ""

    def __str__(self) -> str:
        """
        Returns information about object in human readable format
        """

        TEMPLATE = (
            "Name:          {0}\n"
            "Address:       {1}\n"
            "Port:          {2}\n"
            "Community:     {3}\n"
            "Version:       {4}\n"
        )
        return TEMPLATE.format(
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
    def address(self, new_value: str) -> None:
        if helpers.is_ip_address(new_value):
            self.__address = new_value
        else:
            logging.error("IP address is empty or has an incorrect format.")

    @property
    def community(self) -> str:
        return self.__community

    @community.setter
    def community(self, new_value: str) -> None:
        self.__community = new_value

    @property
    def port(self) -> int:
        return self.__port

    @port.setter
    def port(self, new_value: int) -> None:
        if helpers.is_port_number(new_value):
            self.__version = new_value
        else:
            logging.error("Port number is out of range.")

    @property
    def version(self) -> int:
        return self.__version

    @version.setter
    def version(self, new_value: int) -> None:
        if new_value in NetDevice.__VERSIONS:
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
    def updatetime(self, new_value: int) -> None:
        self.__updatetime = new_value

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
                community=self.__community,
                remote_port=self.__port,
                version=self.__version
            )
            self.__populate()
            return True
        except Exception as err:
            logging.error("Could not connect to device.")
            logging.error(err)

    def get_if_admin_status(self, port: int) -> str:
        """
        Returns admin status of the given interface
        """

        value = self.__get_if_data(
            "IF_ADMIN_STATUS",
            port,
            "Could not get interface admin status."
        )
        return snmp.IF_ADMIN_STATES[value]

    def get_if_description(self, port: int) -> str:
        """
        Returns description of the given interface
        """

        return self.__get_if_data(
            "IF_DESCRIPTION",
            port,
            "Could not get interface description."
        )

    def get_if_in_bandwidth(self, port: int) -> str:
        """
        Returns number of inboud packets on the given interface
        """

        return self.__get_if_data(
            "IF_IN_OCTETS",
            port,
            "Could not get number of inboud bytes."
        )

    def get_if_in_broadcast(self, port: int) -> str:
        """
        Returns number of inbound broadcast packets
        """

        return self.__get_if_data(
            "IF_IN_BROADCAST",
            port,
            "Could not get number of inbound broadcast packets."
        )

    def get_if_in_errors(self, port: int) -> str:
        """
        Returns number of inbound packets that contained errors
        """

        return self.__get_if_data(
            "IF_IN_ERRORS",
            port,
            "Could not get number of inbound packets with errors."
        )

    def get_if_in_discards(self, port: int) -> str:
        """
        Returns number of inbound discard packets
        """

        return self.__get_if_data(
            "IF_IN_DISCARDS",
            port,
            "Could not get number of inbound discard packets."
        )

    def get_if_in_multicast(self, port: int) -> str:
        """
        Returns number of inbound multicast packets
        """

        return self.__get_if_data(
            "IF_IN_MULTICAST",
            port,
            "Could not get number of inbound multicast packets."
        )

    def get_if_in_non_unicast(self, port: int) -> str:
        """
        Returns number of inbound nonunicast packets
        """

        return self.__get_if_data(
            "IF_IN_NON_UNICAST",
            port,
            "Could not get number of inbound nonunicast packets."
        )

    def get_if_in_unicast(self, port: int) -> str:
        """
        Returns number of inbound unicast packets
        """

        return self.__get_if_data(
            "IF_IN_UNICAST",
            port,
            "Could not get number of inbound unicast packets."
        )

    def get_if_last_change(self, port: int) -> str:
        """
        Returns when the given interface entered
        its operational state for the last time
        """

        value = self.__get_if_data(
            "IF_LAST_CHANGE",
            port,
            "Could not get last change time of port number {}.".format(
                str(port)
            )
        )
        return str(timedelta(seconds=(int(value)) / 100))

    def get_if_mtu(self, port: int) -> str:
        """
        Returns mtu value of the given interface
        """

        return self.__get_if_data(
            "IF_MTU",
            port,
            "Could not get mtu value of port number {}.".format(
                str(port)
            )
        )

    def get_if_oper_status(self, port: int) -> str:
        """
        Returns operation status of the given interface
        """

        value = self.__get_if_data(
            "IF_OPER_STATUS",
            port,
            "Could not get interface operation status."
        )
        return snmp.IF_OPER_STATES[value]

    def get_if_out_bandwidth(self, port: int) -> str:
        """
        Returns number of outbound bytes on the given interface
        """

        return self.__get_if_data(
            "IF_OUT_OCTETS",
            port,
            "Could not get number of outboud bytes."
        )

    def get_if_out_broadcast(self, port: int) -> str:
        """
        Returns number of outbound broadcast packets
        """

        return self.__get_if_data(
            "IF_OUT_BROADCAST",
            port,
            "Could not get number of outbound broadcast packets."
        )

    def get_if_out_errors(self, port: int) -> str:
        """
        Returns number of outbound packets that contained errors
        """

        return self.__get_if_data(
            "IF_OUT_ERRORS",
            port,
            "Could not get number of outbound packets with errors."
        )

    def get_if_out_discards(self, port: int) -> str:
        """
        Returns number of outbound discard packets
        """

        return self.__get_if_data(
            "IF_OUT_DISCARDS",
            port,
            "Could not get number of outbound discard packets."
        )

    def get_if_out_multicast(self, port: int) -> str:
        """
        Returns number of outbound multicast packets
        """

        return self.__get_if_data(
            "IF_OUT_MULTICAST",
            port,
            "Could not get number of outbound multicast packets."
        )

    def get_if_out_non_unicast(self, port: int) -> str:
        """
        Returns number of outbound nonunicast packets
        """

        return self.__get_if_data(
            "IF_OUT_NON_UNICAST",
            port,
            "Could not get number of outbound nonunicast packets."
        )

    def get_if_out_unicast(self, port: int) -> str:
        """
        Returns number of outbound unicast packets
        """

        return self.__get_if_data(
            "IF_OUT_UNICAST",
            port,
            "Could not get number of outbound unicast packets."
        )

    def get_if_phys_address(self, port: int, delimiter: str = ":") -> str:
        """
        Returns physical address of the given interface
        """

        result = ""
        if self.__count > 0 and port in self.__indexes:
            if delimiter in NetDevice.__DELIMITERS:
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
                    value = snmp_data.value.strip()
                    if value:
                        result = helpers.get_mac_from_octets(
                            value, delimiter
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
        return result

    def get_if_speed(self, port: int) -> str:
        """
        Returns speed of the given interface
        """

        value = self.__get_if_data(
            "IF_SPEED",
            port,
            "Could not get interface speed."
        )
        result = int(value)
        if result > NetDevice.__COEFFICIENT:
            result = result / NetDevice.__COEFFICIENT
        return str(result)

    def get_if_type(self, port: int) -> str:
        """
        Returns type of the given interface
        """

        value = self.__get_if_data(
            "IF_TYPE",
            port,
            "Could not get interface type."
        )
        return snmp.IF_TYPES[value]

    def get_if_unknown_protos(self, port: int) -> str:
        """
        Returns the number of packets received via the interface which
        were discarded because of an unknown or unsupported protocol
        """

        return self.__get_if_data(
            "IF_UNKNOWN_PROTOS",
            port,
            "Could not get number of packets with unknown protocols."
        )

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

    def __get_if_count(self) -> str:
        """
        Returns number of interfaces
        """

        return self.__get_sys_data(
            "IF_NUMBER",
            "Could not get number of interfaces."
        )

    def __get_description(self) -> str:
        """
        Returns device description
        """

        return self.__get_sys_data(
            "SYS_DECRIPTION",
            "Could not get device description."
        )

    def __get_if_data(
        self,
        snmp_oid: str,
        if_port: int,
        error_msg: str
    ) -> str:
        if self.__count > 0 and if_port in self.__indexes:
            try:
                snmp_data = self.__session.get(
                    snmp.OIDS[snmp_oid] + str(if_port)
                )
            except Exception as err:
                logging.error(error_msg)
                logging.error(err)
            else:
                return snmp_data.value
        else:
            logging.error(
                "No interface or given interface number is incorrect."
            )

    def __get_if_indexes(self) -> List[int]:
        """
        Returns list of interfaces indexes
        """

        try:
            interfaces = self.__session.walk(snmp.OIDS["IF_INDEX"])
        except Exception as err:
            logging.error("Could not get list of interface indexes.")
            logging.error(err)
        else:
            result = []
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

    def __get_sys_data(self, snmp_oid: str, error_msg: str) -> str:
        try:
            snmp_data = self.__session.get(
                snmp.OIDS[snmp_oid]
            )
        except Exception as err:
            logging.error(error_msg)
            logging.error(err)
        else:
            return snmp_data.value

    def __get_uptime(self) -> str:
        """
        Returns device uptime
        """

        value = self.__get_sys_data(
            "SYS_UPTIME",
            "Could not get device uptime."
        )
        # Value is the time (in hundredths of a second) since the
        # network management portion of the system was last re-initialized
        return str(timedelta(seconds=(int(value)) / 100))
