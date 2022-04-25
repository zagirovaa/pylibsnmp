#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from __future__ import annotations
from typing import Dict


# OIDs (Object IDentifiers) used in library
OIDS: Dict[str, str] = {
    "SYS_DECRIPTION":       "1.3.6.1.2.1.1.1.0",
    "SYS_UPTIME":           "1.3.6.1.2.1.1.3.0",
    "SYS_CONTACT":          "1.3.6.1.2.1.1.4.0",
    "SYS_NAME":             "1.3.6.1.2.1.1.5.0",
    "SYS_LOCATION":         "1.3.6.1.2.1.1.6.0",
    "IF_NUMBER":            "1.3.6.1.2.1.2.1.0",
    "IF_INDEX":             "1.3.6.1.2.1.2.2.1.1.",
    "IF_DESCRIPTION":       "1.3.6.1.2.1.2.2.1.2.",
    "IF_TYPE":              "1.3.6.1.2.1.2.2.1.3.",
    "IF_MTU":               "1.3.6.1.2.1.2.2.1.4.",
    "IF_SPEED":             "1.3.6.1.2.1.2.2.1.5.",
    "IF_PHYS_ADDRESS":      "1.3.6.1.2.1.2.2.1.6.",
    "IF_ADMIN_STATUS":      "1.3.6.1.2.1.2.2.1.7.",
    "IF_OPER_STATUS":       "1.3.6.1.2.1.2.2.1.8.",
    # "IF_LAST_CHANGE":       "1.3.6.1.2.1.2.2.1.9.",
    "IF_IN_OCTETS":         "1.3.6.1.2.1.2.2.1.10.",
    # "IF_IN_UNICAST":        "1.3.6.1.2.1.2.2.1.11.",
    # "IF_IN_NON_UNICAST":    "1.3.6.1.2.1.2.2.1.12.",
    # "IF_IN_DISCARDS":       "1.3.6.1.2.1.2.2.1.13.",
    # "IF_IN_ERRORS":         "1.3.6.1.2.1.2.2.1.14.",
    # "IF_UNKNOWN_PROTOS":    "1.3.6.1.2.1.2.2.1.15.",
    "IF_OUT_OCTETS":        "1.3.6.1.2.1.2.2.1.16.",
    # "IF_OUT_UNICAST":       "1.3.6.1.2.1.2.2.1.17.",
    # "IF_OUT_NON_UNICAST":   "1.3.6.1.2.1.2.2.1.18.",
    # "IF_OUT_DISCARDS":      "1.3.6.1.2.1.2.2.1.19.",
    # "IF_OUT_ERRORS":        "1.3.6.1.2.1.2.2.1.20.",
    # "IF_IN_MULTICAST":      "1.3.6.1.2.1.31.1.1.1.2.",
    # "IF_IN_BROADCAST":      "1.3.6.1.2.1.31.1.1.1.3.",
    # "IF_OUT_MULTICAST":     "1.3.6.1.2.1.31.1.1.1.4.",
    # "IF_OUT_BROADCAST":     "1.3.6.1.2.1.31.1.1.1.5."
}

# The type of interface, distinguished according to
# the physical/link protocol(s) immediately `below'
# the network layer in the protocol stack
IF_TYPES: Dict[str, str] = {
    "1":    "other",
    "2":    "regular1822",
    "3":    "hdh1822",
    "4":    "ddn-x25",
    "5":    "rfc877-x25",
    "6":    "ethernet-csmacd",
    "7":    "iso88023-csmacd",
    "8":    "iso88024-tokenBus",
    "9":    "iso88025-tokenRing",
    "10":   "iso88026-man",
    "11":   "starLan",
    "12":   "proteon-10Mbit",
    "13":   "proteon-80Mbit",
    "14":   "hyperchannel",
    "15":   "fddi",
    "16":   "lapb",
    "17":   "sdlc",
    "18":   "ds1",
    "19":   "e1",
    "20":   "basicISDN",
    "21":   "primaryISDN",
    "22":   "propPointToPointSerial",
    "23":   "ppp",
    "24":   "softwareLoopback",
    "25":   "eon",
    "26":   "ethernet-3Mbit",
    "27":   "nsip",
    "28":   "slip",
    "29":   "ultra",
    "30":   "ds3",
    "31":   "sip",
    "32":   "frame-relay",
    "33":   "rs232",
    "34":   "para",
    "35":   "arcnet",
    "36":   "arcnetPlus",
    "37":   "atm",
    "38":   "miox25",
    "39":   "sonet",
    "40":   "x25ple",
    "41":   "iso88022llc",
    "42":   "localTalk",
    "43":   "smdsDxi",
    "44":   "frameRelayService",
    "45":   "v35",
    "46":   "hssi",
    "47":   "hippi",
    "48":   "modem",
    "49":   "aal5",
    "50":   "sonetPath",
    "51":   "sonetVT",
    "52":   "smdsIcip",
    "53":   "propVirtual",
    "54":   "propMultiplexor",
    "55":   "ieee80212",
    "56":   "fibreChannel",
    "57":   "hippiInterface",
    "58":   "frameRelayInterconnect",
    "59":   "aflane8023",
    "60":   "aflane8025",
    "61":   "cctEmul",
    "62":   "fastEther",
    "63":   "isdn",
    "64":   "v11",
    "65":   "v36",
    "66":   "g703at64k",
    "67":   "g703at2mb",
    "68":   "qllc",
    "69":   "fastEtherFX",
    "70":   "channel",
    "71":   "ieee80211",
    "72":   "ibm370parChan",
    "73":   "escon",
    "74":   "dlsw",
    "75":   "isdns",
    "76":   "isdnu",
    "77":   "lapd",
    "78":   "ipSwitch",
    "79":   "rsrb",
    "80":   "atmLogical",
    "81":   "ds0",
    "82":   "ds0Bundle",
    "83":   "bsc",
    "84":   "async",
    "85":   "cnr",
    "86":   "iso88025Dtr",
    "87":   "eplrs",
    "88":   "arap",
    "89":   "propCnls",
    "90":   "hostPad",
    "91":   "termPad",
    "92":   "frameRelayMPI",
    "93":   "x213",
    "94":   "adsl",
    "95":   "radsl",
    "96":   "sdsl",
    "97":   "vdsl",
    "98":   "iso88025CRFPInt",
    "99":   "myrinet",
    "100":  "voiceEM"
    #    voiceFXO(101),      -- voice Foreign Exchange Office
    #    voiceFXS(102),      -- voice Foreign Exchange Station
    #    voiceEncap(103),    -- voice encapsulation
    #    voiceOverIp(104),   -- voice over IP encapsulation
    #    atmDxi(105),        -- ATM DXI
    #    atmFuni(106),       -- ATM FUNI
    #    atmIma (107),       -- ATM IMA
    #    pppMultilinkBundle(108), -- PPP Multilink Bundle
    #    ipOverCdlc (109),   -- IBM ipOverCdlc
    #    ipOverClaw (110),   -- IBM Common Link Access to Workstn
    #    stackToStack (111), -- IBM stackToStack
    #    virtualIpAddress (112), -- IBM VIPA
    #    mpc (113),          -- IBM multi-protocol channel support
    #    ipOverAtm (114),    -- IBM ipOverAtm
    #    iso88025Fiber (115), -- ISO 802.5j Fiber Token Ring
    #    tdlc (116),	       -- IBM twinaxial data link control
    #    gigabitEthernet (117), -- Obsoleted via RFC3635
    #                           -- ethernetCsmacd (6) should be used instead
    #    hdlc (118),         -- HDLC
    #    lapf (119),	       -- LAP F
    #    v37 (120),	       -- V.37
    #    x25mlp (121),       -- Multi-Link Protocol
    #    x25huntGroup (122), -- X25 Hunt Group
    #    transpHdlc (123),   -- Transp HDLC
    #    interleave (124),   -- Interleave channel
    #    fast (125),         -- Fast channel
    #    ip (126),	       -- IP (for APPN HPR in IP networks)
    #    docsCableMaclayer (127),  -- CATV Mac Layer
    #    docsCableDownstream (128), -- CATV Downstream interface
    #    docsCableUpstream (129),  -- CATV Upstream interface
    #    a12MppSwitch (130), -- Avalon Parallel Processor
    #    tunnel (131),       -- Encapsulation interface
    #    coffee (132),       -- coffee pot
    #    ces (133),          -- Circuit Emulation Service
    #    atmSubInterface (134), -- ATM Sub Interface
    #    l2vlan (135),       -- Layer 2 Virtual LAN using 802.1Q
    #    l3ipvlan (136),     -- Layer 3 Virtual LAN using IP
    #    l3ipxvlan (137),    -- Layer 3 Virtual LAN using IPX
    #    digitalPowerline (138), -- IP over Power Lines
    #    mediaMailOverIp (139), -- Multimedia Mail over IP
    #    dtm (140),        -- Dynamic syncronous Transfer Mode
    #    dcn (141),    -- Data Communications Network
    #    ipForward (142),    -- IP Forwarding Interface
    #    msdsl (143),       -- Multi-rate Symmetric DSL
    #    ieee1394 (144), -- IEEE1394 High Performance Serial Bus
    #    if-gsn (145),       --   HIPPI-6400
    #    dvbRccMacLayer (146), -- DVB-RCC MAC Layer
    #    dvbRccDownstream (147),  -- DVB-RCC Downstream Channel
    #    dvbRccUpstream (148),  -- DVB-RCC Upstream Channel
    #    atmVirtual (149),   -- ATM Virtual Interface
    #    mplsTunnel (150),   -- MPLS Tunnel Virtual Interface
    #    srp (151),	-- Spatial Reuse Protocol
    #    voiceOverAtm (152),  -- Voice Over ATM
    #    voiceOverFrameRelay (153),   -- Voice Over Frame Relay
    #    idsl (154),		-- Digital Subscriber Loop over ISDN
    #    compositeLink (155),  -- Avici Composite Link Interface
    #    ss7SigLink (156),     -- SS7 Signaling Link
    #    propWirelessP2P (157),  --  Prop. P2P wireless interface
    #    frForward (158),    -- Frame Forward Interface
    #    rfc1483 (159),	-- Multiprotocol over ATM AAL5
    #    usb (160),		-- USB Interface
    #    ieee8023adLag (161),  -- IEEE 802.3ad Link Aggregate
    #    bgppolicyaccounting (162), -- BGP Policy Accounting
    #    frf16MfrBundle (163), -- FRF .16 Multilink Frame Relay
    #    h323Gatekeeper (164), -- H323 Gatekeeper
    #    h323Proxy (165), -- H323 Voice and Video Proxy
    #    mpls (166), -- MPLS
    #    mfSigLink (167), -- Multi-frequency signaling link
    #    hdsl2 (168), -- High Bit-Rate DSL - 2nd generation
    #    shdsl (169), -- Multirate HDSL2
    #    ds1FDL (170), -- Facility Data Link 4Kbps on a DS1
    #    pos (171), -- Packet over SONET/SDH Interface
    #    dvbAsiIn (172), -- DVB-ASI Input
    #    dvbAsiOut (173), -- DVB-ASI Output
    #    plc (174), -- Power Line Communtications
    #    nfas (175), -- Non Facility Associated Signaling
    #    tr008 (176), -- TR008
    #    gr303RDT (177), -- Remote Digital Terminal
    #    gr303IDT (178), -- Integrated Digital Terminal
    #    isup (179), -- ISUP
    #    propDocsWirelessMaclayer (180), -- Cisco proprietary Maclayer
    #    propDocsWirelessDownstream (181), -- Cisco proprietary Downstream
    #    propDocsWirelessUpstream (182), -- Cisco proprietary Upstream
    #    hiperlan2 (183), -- HIPERLAN Type 2 Radio Interface
    #    propBWAp2Mp (184), -- PropBroadbandWirelessAccesspt2multipt
    #              -- use of this iftype for IEEE 802.16 WMAN
    #              -- interfaces as per IEEE Std 802.16f is
    #              -- deprecated and ifType 237 should be used instead.
    #    sonetOverheadChannel (185), -- SONET Overhead Channel
    #    digitalWrapperOverheadChannel (186), -- Digital Wrapper
    #    aal2 (187), -- ATM adaptation layer 2
    #    radioMAC (188), -- MAC layer over radio links
    #    atmRadio (189), -- ATM over radio links
    #    imt (190), -- Inter Machine Trunks
    #    mvl (191), -- Multiple Virtual Lines DSL
    #    reachDSL (192), -- Long Reach DSL
    #    frDlciEndPt (193), -- Frame Relay DLCI End Point
    #    atmVciEndPt (194), -- ATM VCI End Point
    #    opticalChannel (195), -- Optical Channel
    #    opticalTransport (196), -- Optical Transport
    #    propAtm (197), --  Proprietary ATM
    #    voiceOverCable (198), -- Voice Over Cable Interface
    #    infiniband (199), -- Infiniband
    #    teLink (200), -- TE Link
    #    q2931 (201), -- Q.2931
    #    virtualTg (202), -- Virtual Trunk Group
    #    sipTg (203), -- SIP Trunk Group
    #    sipSig (204), -- SIP Signaling
    #    docsCableUpstreamChannel (205), -- CATV Upstream Channel
    #    econet (206), -- Acorn Econet
    #    pon155 (207), -- FSAN 155Mb Symetrical PON interface
    #    pon622 (208), -- FSAN622Mb Symetrical PON interface
    #    bridge (209), -- Transparent bridge interface
    #    linegroup (210), -- Interface common to multiple lines
    #    voiceEMFGD (211), -- voice E&M Feature Group D
    #    voiceFGDEANA (212), -- voice FGD Exchange Access North American
    #    voiceDID (213), -- voice Direct Inward Dialing
    #    mpegTransport (214), -- MPEG transport interface
    #    sixToFour (215), -- 6to4 interface (DEPRECATED)
    #    gtp (216), -- GTP (GPRS Tunneling Protocol)
    #    pdnEtherLoop1 (217), -- Paradyne EtherLoop 1
    #    pdnEtherLoop2 (218), -- Paradyne EtherLoop 2
    #    opticalChannelGroup (219), -- Optical Channel Group
    #    homepna (220), -- HomePNA ITU-T G.989
    #    gfp (221), -- Generic Framing Procedure (GFP)
    #    ciscoISLvlan (222), -- Layer 2 Virtual LAN using Cisco ISL
    #    actelisMetaLOOP (223), -- Acteleis proprietary MetaLOOP High Speed Link
    #    fcipLink (224), -- FCIP Link
    #    rpr (225), -- Resilient Packet Ring Interface Type
    #    qam (226), -- RF Qam Interface
    #    lmp (227), -- Link Management Protocol
    #    cblVectaStar (228), -- Cambridge Broadband Networks Limited VectaStar
    #    docsCableMCmtsDownstream (229), -- CATV Modular CMTS Downstream Interface
    #    adsl2 (230), -- Asymmetric Digital Subscriber Loop Version 2
    #                 -- (DEPRECATED/OBSOLETED - please use adsl2plus 238 instead)
    #    macSecControlledIF (231), -- MACSecControlled
    #    macSecUncontrolledIF (232), -- MACSecUncontrolled
    #    aviciOpticalEther (233), -- Avici Optical Ethernet Aggregate
    #    atmbond (234), -- atmbond
    #    voiceFGDOS (235), -- voice FGD Operator Services
    #    mocaVersion1 (236), -- MultiMedia over Coax Alliance (MoCA) Interface
    #              -- as documented in information provided privately to IANA
    #    ieee80216WMAN (237), -- IEEE 802.16 WMAN interface
    #    adsl2plus (238), -- Asymmetric Digital Subscriber Loop Version 2,
    #                    -- Version 2 Plus and all variants
    #    dvbRcsMacLayer (239), -- DVB-RCS MAC Layer
    #    dvbTdm (240), -- DVB Satellite TDM
    #    dvbRcsTdma (241), -- DVB-RCS TDMA
    #    x86Laps (242), -- LAPS based on ITU-T X.86/Y.1323
    #    wwanPP (243), -- 3GPP WWAN
    #    wwanPP2 (244), -- 3GPP2 WWAN
    #    voiceEBS (245), -- voice P-phone EBS physical interface
    #    ifPwType (246), -- Pseudowire interface type
    #    ilan (247), -- Internal LAN on a bridge per IEEE 802.1ap
    #    pip (248), -- Provider Instance Port on a bridge per IEEE 802.1ah PBB
    #    aluELP (249), -- Alcatel-Lucent Ethernet Link Protection
    #    gpon (250), -- Gigabit-capable passive optical networks (G-PON) as per ITU-T G.948
    #    vdsl2 (251), -- Very high speed digital subscriber line Version 2 (as per ITU-T Recommendation G.993.2)
    #    capwapDot11Profile (252), -- WLAN Profile Interface
    #    capwapDot11Bss (253), -- WLAN BSS Interface
    #    capwapWtpVirtualRadio (254), -- WTP Virtual Radio Interface
    #    bits (255), -- bitsport
    #    docsCableUpstreamRfPort (256), -- DOCSIS CATV Upstream RF Port
    #    cableDownstreamRfPort (257), -- CATV downstream RF port
    #    vmwareVirtualNic (258), -- VMware Virtual Network Interface
    #    ieee802154 (259), -- IEEE 802.15.4 WPAN interface
    #    otnOdu (260), -- OTN Optical Data Unit
    #    otnOtu (261), -- OTN Optical channel Transport Unit
    #    ifVfiType (262), -- VPLS Forwarding Instance Interface Type
    #    g9981 (263), -- G.998.1 bonded interface
    #    g9982 (264), -- G.998.2 bonded interface
    #    g9983 (265), -- G.998.3 bonded interface
    #    aluEpon (266), -- Ethernet Passive Optical Networks (E-PON)
    #    aluEponOnu (267), -- EPON Optical Network Unit
    #    aluEponPhysicalUni (268), -- EPON physical User to Network interface
    #    aluEponLogicalLink (269), -- The emulation of a point-to-point link over the EPON layer
    #    aluGponOnu (270), -- GPON Optical Network Unit
    #    aluGponPhysicalUni (271), -- GPON physical User to Network interface
    #    vmwareNicTeam (272), -- VMware NIC Team
    #    docsOfdmDownstream (277), -- CATV Downstream OFDM interface
    #    docsOfdmaUpstream (278), -- CATV Upstream OFDMA interface
    #    gfast (279), -- G.fast port
    #    sdci (280), -- SDCI (IO-Link)
    #    xboxWireless (281), -- Xbox wireless
    #    fastdsl (282), -- FastDSL
    #    docsCableScte55d1FwdOob (283), -- Cable SCTE 55-1 OOB Forward Channel
    #    docsCableScte55d1RetOob (284), -- Cable SCTE 55-1 OOB Return Channel
    #    docsCableScte55d2DsOob (285), -- Cable SCTE 55-2 OOB Downstream Channel
    #    docsCableScte55d2UsOob (286), -- Cable SCTE 55-2 OOB Upstream Channel
    #    docsCableNdf (287), -- Cable Narrowband Digital Forward
    #    docsCableNdr (288), -- Cable Narrowband Digital Return
    #    ptm (289), -- Packet Transfer Mode
    #    ghn (290), -- G.hn port
    #    otnOtsi (291), -- Optical Tributary Signal
    #    otnOtuc (292), -- OTN OTUCn
    #    otnOduc (293), -- OTN ODUC
    #    otnOtsig (294), -- OTN OTUC Signal
    #    microwaveCarrierTermination (295), -- air interface of a single microwave carrier
    #    microwaveRadioLinkTerminal (296), -- radio link interface for one or several aggregated microwave carriers
    #    ieee8021axDrni (297), -- IEEE 802.1AX Distributed Resilient Network Interface
    #    ax25 (298), -- AX.25 network interfaces
    #    ieee19061nanocom (299), -- Nanoscale and Molecular Communication
    #    cpri (300), -- Common Public Radio Interface
    #    omni (301), -- Overlay Multilink Network Interface (OMNI)
    #    roe (302), -- Radio over Ethernet Interface
    #    p2pOverLan (303) -- Point to Point over LAN interface
}

# The desired admin state of the interface.
# The testing(3) state indicates that no
# operational packets can be passed.
IF_ADMIN_STATES: Dict[str, str] = {
    "1": "up",
    "2": "down",
    "3": "testing"
}

# The desired operational state of the interface.
# The testing(3) state indicates that no
# operational packets can be passed.
IF_OPER_STATES: Dict[str, str] = {
    "1": "up",
    "2": "down",
    "3": "testing",
    "4": "unknown",
    "5": "dormant",
    "6": "notPresent",
    "7": "lowerLayerDown"
}
