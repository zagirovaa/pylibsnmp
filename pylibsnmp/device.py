#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
Python module with NetDevice class used
to create network devices with SNMP protocol enabled.

SNMP v1 and v2 are supported.

Pass ip address, snmp community, port and version in order
to be able to initialize the connection with the device.

IP address is required while snmp community, port and version are optional.
"""


from __future__ import annotations
from datetime import timedelta
import logging
from typing import List

from easysnmp import Session

from . import snmp
from . import helpers


class NetDevice:
    """
    Class for creating snmp enabled network devices.
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
        Class constructor.

        params:
            | address: {str} - device ip address
            | community: {str} - snmp community {default: "public"}
            | port: {int} - snmp port {default: 161}
            | version: {int} - snmp version {default: 2}
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
        self.__description = ""
        self.__indexes = []
        self.__location = ""
        self.__name = ""
        self.__number = 0
        self.__repeat = None
        self.__session = None
        self.__types = []
        # Each 60 seconds device related data will be populated
        self.__updatetime = 60
        self.__uptime = ""

    def __str__(self) -> str:
        """
        Returns information about object in human readable format.
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
        """IP address"""

        return self.__address

    @address.setter
    def address(self, new_value: str) -> None:
        if helpers.is_ip_address(new_value):
            self.__address = new_value
        else:
            logging.error("IP address is empty or has an incorrect format.")

    @property
    def community(self) -> str:
        """SNMP community"""

        return self.__community

    @community.setter
    def community(self, new_value: str) -> None:
        self.__community = new_value

    @property
    def port(self) -> int:
        """SNMP port"""

        return self.__port

    @port.setter
    def port(self, new_value: int) -> None:
        if helpers.is_port_number(new_value):
            self.__version = new_value
        else:
            logging.error("Port number is out of range.")

    @property
    def version(self) -> int:
        """SNMP version"""

        return self.__version

    @version.setter
    def version(self, new_value: int) -> None:
        if new_value in NetDevice.__VERSIONS:
            self.__version = new_value
        else:
            logging.error("Incorrect format or unsupported version of snmp.")

    @property
    def autoupdate(self) -> bool:
        """Enable/disable device information autoupdate"""

        return self.__autoupdate

    @autoupdate.setter
    def autoupdate(self, new_value: bool) -> None:
        self.__autoupdate = new_value
        self.__change_autoupdate()

    @property
    def contact(self) -> str:
        """Contact"""

        return self.__contact

    @property
    def description(self) -> str:
        """Description"""

        return self.__description

    @property
    def indexes(self) -> List[int]:
        """List of interface numbers"""

        return self.__indexes

    @property
    def location(self) -> str:
        """Location"""

        return self.__location

    @property
    def name(self) -> str:
        """Name"""

        return self.__name

    @property
    def number(self) -> int:
        return self.__number

    @property
    def types(self) -> List[str]:
        """List of interface types"""

        return self.__types

    @property
    def updatetime(self) -> int:
        """Autoupdate interval"""

        return self.__updatetime

    @updatetime.setter
    def updatetime(self, new_value: int) -> None:
        self.__updatetime = new_value
        self.__change_autoupdate()

    @property
    def uptime(self) -> str:
        """Uptime"""

        return self.__uptime

    # ----------------------------------
    # Public methods declaration section
    # ----------------------------------
    def connect(self) -> bool:
        """
        Initiates connection with the device
        using parameters passed in constructor.
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

    def disconnect(self) -> None:
        """
        Correctly drops connection with the device.
        """

        try:
            self.__repeat.cancel()
            self.__repeat = None
        except Exception as err:
            logging.error("Could not disconnect device.")
            logging.error(err)

    def get_if_admin_status(self, port: int) -> str:
        """
        The desired state of the interface. The testing(3) state indicates
        that no operational packets can be passed. When a managed system
        initializes, all interfaces start with ifAdminStatus in the down(2)
        state. As a result of either explicit management action or per
        configuration information retained by the managed system,
        ifAdminStatus is then changed to either the up(1) or testing(3)
        states (or remains in the down(2) state).
        """

        value = self.__get_if_data(
            "IF_ADMIN_STATUS",
            port,
            "Could not get interface admin status."
        )
        return snmp.IF_ADMIN_STATES[value]

    def get_if_description(self, port: int) -> str:
        """
        A textual string containing information about the interface.
        This string should include the name of the manufacturer,
        the product name and the version of the interface hardware/software.
        """

        return self.__get_if_data(
            "IF_DESCRIPTION",
            port,
            "Could not get interface description."
        )

    def get_if_in_octets(self, port: int) -> str:
        """
        The total number of octets received on the interface,
        including framing characters.
        """

        return self.__get_if_data(
            "IF_IN_OCTETS",
            port,
            "Could not get number of inboud bytes."
        )

    def get_if_in_broadcast(self, port: int) -> str:
        """
        The number of packets, delivered by this sub-layer to a
        higher (sub-)layer, which were addressed to a broadcast
        address at this sub-layer. This object is a 64-bit version
        of ifInBroadcastPkts.
        """

        return self.__get_if_data(
            "IF_IN_BROADCAST",
            port,
            "Could not get number of inbound broadcast packets."
        )

    def get_if_in_errors(self, port: int) -> str:
        """
        For packet-oriented interfaces, the number of inbound packets
        that contained errors preventing them from being deliverable to a
        higher-layer protocol. For character-oriented or fixed-length
        interfaces, the number of inbound transmission units that contained
        errors preventing them from being deliverable to a higher-layer
        protocol.
        """

        return self.__get_if_data(
            "IF_IN_ERRORS",
            port,
            "Could not get number of inbound packets with errors."
        )

    def get_if_in_discards(self, port: int) -> str:
        """
        The number of inbound packets which were chosen to be discarded even
        though no errors had been detected to prevent their being deliverable
        to a higher-layer protocol. One possible reason for discarding such a
        packet could be to free up buffer space.
        """

        return self.__get_if_data(
            "IF_IN_DISCARDS",
            port,
            "Could not get number of inbound discard packets."
        )

    def get_if_in_multicast(self, port: int) -> str:
        """
        The number of packets, delivered by this sub-layer to a higher
        (sub-)layer, which were addressed to a multicast address at this
        sub-layer. For a MAC layer protocol, this includes both Group and
        Functional addresses. This object is a 64-bit version of
        ifInMulticastPkts.
        """

        return self.__get_if_data(
            "IF_IN_MULTICAST",
            port,
            "Could not get number of inbound multicast packets."
        )

    def get_if_in_non_unicast(self, port: int) -> str:
        """
        The number of packets, delivered by this sub-layer to a higher
        (sub-)layer, which were addressed to a multicast or broadcast address
        at this sub-layer.
        """

        return self.__get_if_data(
            "IF_IN_NON_UNICAST",
            port,
            "Could not get number of inbound nonunicast packets."
        )

    def get_if_in_unicast(self, port: int) -> str:
        """
        The number of packets, delivered by this sub-layer to a higher
        (sub-)layer, which were not addressed to a multicast or broadcast
        address at this sub-layer.
        """

        return self.__get_if_data(
            "IF_IN_UNICAST",
            port,
            "Could not get number of inbound unicast packets."
        )

    def get_if_last_change(self, port: int) -> str:
        """
        The value of sysUpTime at the time the interface entered its current
        operational state. If the current state was entered prior to the last
        re-initialization of the local network management subsystem, then this
        object contains a zero value.
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
        The size of the largest packet which can be sent/received on the
        interface, specified in octets. For interfaces that are used for
        transmitting network datagrams, this is the size of the largest
        network datagram that can be sent on the interface.
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
        The current operational state of the interface. The testing(3) state
        indicates that no operational packets can be passed. If ifAdminStatus
        is down(2) then ifOperStatus should be down(2). If ifAdminStatus is
        changed to up(1) then ifOperStatus should change to up(1) if the
        interface is ready to transmit and receive network traffic; it should
        change to dormant(5) if the interface is waiting for external actions
        (such as a serial line waiting for an incoming connection); it should
        remain in the down(2) state if and only if there is a fault that
        prevents it from going to the up(1) state; it should remain in the
        notPresent(6) state if the interface has missing (typically, hardware)
        components.
        """

        value = self.__get_if_data(
            "IF_OPER_STATUS",
            port,
            "Could not get interface operation status."
        )
        return snmp.IF_OPER_STATES[value]

    def get_if_out_octets(self, port: int) -> str:
        """
        The total number of octets transmitted out of the interface, including
        framing characters.
        """

        return self.__get_if_data(
            "IF_OUT_OCTETS",
            port,
            "Could not get number of outboud bytes."
        )

    def get_if_out_broadcast(self, port: int) -> str:
        """
        The total number of packets that higher-level protocols requested be
        transmitted, and which were addressed to a broadcast address at this
        sub-layer, including those that were discarded or not sent. This object
        is a 64-bit version of ifOutBroadcastPkts.
        """

        return self.__get_if_data(
            "IF_OUT_BROADCAST",
            port,
            "Could not get number of outbound broadcast packets."
        )

    def get_if_out_errors(self, port: int) -> str:
        """
        For packet-oriented interfaces, the number of outbound packets that
        could not be transmitted because of errors. For character-oriented or
        fixed-length interfaces, the number of outbound transmission units that
        could not be transmitted because of errors.
        """

        return self.__get_if_data(
            "IF_OUT_ERRORS",
            port,
            "Could not get number of outbound packets with errors."
        )

    def get_if_out_discards(self, port: int) -> str:
        """
        The number of outbound packets which were chosen to be discarded even
        though no errors had been detected to prevent their being transmitted.
        One possible reason for discarding such a packet could be to free up
        buffer space.
        """

        return self.__get_if_data(
            "IF_OUT_DISCARDS",
            port,
            "Could not get number of outbound discard packets."
        )

    def get_if_out_multicast(self, port: int) -> str:
        """
        The total number of packets that higher-level protocols requested be
        transmitted, and which were addressed to a multicast address at this
        sub-layer, including those that were discarded or not sent. For a MAC
        layer protocol, this includes both Group and Functional addresses. This
        object is a 64-bit version of ifOutMulticastPkts.
        """

        return self.__get_if_data(
            "IF_OUT_MULTICAST",
            port,
            "Could not get number of outbound multicast packets."
        )

    def get_if_out_non_unicast(self, port: int) -> str:
        """
        The total number of packets that higher-level protocols requested be
        transmitted, and which were addressed to a multicast or broadcast
        address at this sub-layer, including those that were discarded or
        not sent.
        """

        return self.__get_if_data(
            "IF_OUT_NON_UNICAST",
            port,
            "Could not get number of outbound nonunicast packets."
        )

    def get_if_out_unicast(self, port: int) -> str:
        """
        The total number of packets that higher-level protocols requested be
        transmitted, and which were not addressed to a multicast or broadcast
        address at this sub-layer, including those that were discarded or
        not sent.
        """

        return self.__get_if_data(
            "IF_OUT_UNICAST",
            port,
            "Could not get number of outbound unicast packets."
        )

    def get_if_phys_address(self, port: int, delimiter: str = ":") -> str:
        """
        The interface's address at its protocol sub-layer. For example, for an
        802.x interface, this object normally contains a MAC address. The
        interface's media-specific MIB must define the bit and byte ordering
        and the format of the value of this object. For interfaces which do not
        have such an address (e.g., a serial line), this object should contain
        an octet string of zero length.
        """

        result = ""
        if self.__number > 0 and port in self.__indexes:
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
        An estimate of the interface's current bandwidth in bits per second.
        For interfaces which do not vary in bandwidth or for those where no
        accurate estimation can be made, this object should contain the nominal
        bandwidth. If the bandwidth of the interface is greater than the
        maximum value reportable by this object then this object should report
        its maximum value (4,294,967,295) and ifHighSpeed must be used to
        report the interace's speed. For a sub-layer which has no concept of
        bandwidth, this object should be zero.
        """

        value = self.__get_if_data(
            "IF_SPEED",
            port,
            "Could not get interface speed."
        )
        result = int(value)
        if result > NetDevice.__COEFFICIENT:
            result = int(result / NetDevice.__COEFFICIENT)
        return str(result)

    def get_if_type(self, port: int) -> str:
        """
        The type of interface. Additional values for ifType are assigned by the
        Internet Assigned Numbers Authority (IANA), through updating the syntax
        of the IANAifType textual convention.
        """

        value = self.__get_if_data(
            "IF_TYPE",
            port,
            "Could not get interface type."
        )
        return snmp.IF_TYPES[value]

    def get_if_unknown_protos(self, port: int) -> str:
        """
        For packet-oriented interfaces, the number of packets received via the
        interface which were discarded because of an unknown or unsupported
        protocol. For character-oriented or fixed-length interfaces that
        support protocol multiplexing the number of transmission units received
        via the interface which were discarded because of an unknown or
        unsupported protocol. For any interface that does not support protocol
        multiplexing, this counter will always be 0.
        """

        return self.__get_if_data(
            "IF_UNKNOWN_PROTOS",
            port,
            "Could not get number of packets with unknown protocols."
        )

    # -----------------------------------
    # Рrivate methods declaration section
    # -----------------------------------
    def __change_autoupdate(self):
        """
        Function activates/deactivates autoupdate functionality.
        """

        if self.__autoupdate:
            self.__repeat = helpers.SetInterval(
                self.__populate,
                self.__updatetime
            )
        elif self.__repeat is not None:
            self.__repeat.cancel()
            self.__repeat = None

    def __get_contact(self) -> str:
        """
        The textual identification of the contact person for this managed node,
        together with information on how to contact this person.
        """

        return self.__get_sys_data(
            "SYS_CONTACT",
            "Could not get device contact."
        )

    def __get_description(self) -> str:
        """
        A textual description of the entity. This value should include the full
        name and version identification of the system's hardware type, software
        operating-system, and networking software. It is mandatory that this
        only contain printable ASCII characters.
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
        """
        Function used in receiving interface related information.
        """

        if self.__number > 0 and if_port in self.__indexes:
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
        A unique value, greater than zero, for each interface. It is
        recommended that values are assigned contiguously starting from 1. The
        value for each interface sub-layer must remain constant at least from
        one re-initialization of the entity's network management system to the
        next re-initialization.
        """

        try:
            interfaces = self.__session.walk(snmp.OIDS["IF_INDEX"])
        except Exception as err:
            logging.error("Could not get list of interface indexes.")
            logging.error(err)
        else:
            return [int(interface.value) for interface in interfaces]

    def __get_if_number(self) -> str:
        """
        The number of network interfaces (regardless of their current state)
        present on this system.
        """

        return self.__get_sys_data(
            "IF_NUMBER",
            "Could not get number of interfaces."
        )

    def __get_if_types(self) -> List[str]:
        """
        Returns list of interface types.
        """

        result = []
        for index in self.__indexes:
            if_type = self.get_if_type(index)
            if if_type not in result:
                result.append(if_type)
        return result

    def __get_location(self) -> str:
        """
        The physical location of this node
        (e.g., "telephone closet, 3rd floor").
        """

        return self.__get_sys_data(
            "SYS_LOCATION",
            "Could not get device location."
        )

    def __get_name(self) -> str:
        """
        An administratively-assigned name for this managed node. By convention,
        this is the node's fully-qualified domain name.
        """

        return self.__get_sys_data(
            "SYS_NAME",
            "Could not get device name."
        )

    def __get_sys_data(self, snmp_oid: str, error_msg: str) -> str:
        """
        Function used in receiving device related information.
        """

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
        The time (in hundredths of a second) since the network management
        portion of the system was last re-initialized.
        """

        value = self.__get_sys_data(
            "SYS_UPTIME",
            "Could not get device uptime."
        )
        # Value is the time (in hundredths of a second) since the
        # network management portion of the system was last re-initialized
        return str(timedelta(seconds=(int(value)) / 100))

    def __populate(self) -> None:
        """
        Populates device fields with necessary data.
        """

        self.__number = int(self.__get_if_number())
        self.__contact = self.__get_contact()
        self.__description = self.__get_description()
        self.__indexes = self.__get_if_indexes()
        self.__location = self.__get_location()
        self.__name = self.__get_name()
        self.__types = self.__get_if_types()
        self.__uptime = self.__get_uptime()
