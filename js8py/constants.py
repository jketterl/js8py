alphanumeric = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ /@"  # callsign and grid alphabet
alphabet72 = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-+/?."

directed_cmds = {
    "HB":           -1,  # this is my heartbeat (unused except for faux processing of HBs as directed commands)
    "SNR?":          0,  # query snr
    "?":             0,  # compat
    "DIT DIT":       1,  # unused
    "NACK":          2,  # negative acknowledge
    "HEARING?":      3,  # query station calls heard
    "GRID?":         4,  # query grid
    ">":             5,  # relay message
    "STATUS?":       6,  # query idle message
    "STATUS":        7,  # this is my status
    "HEARING":       8,  # these are the stations i'm hearing
    "MSG":           9,  # this is a complete message
    "MSG TO:":      10,  # store message at a station
    "QUERY":        11,  # generic query
    "QUERY MSGS":   12,  # do you have any stored messages?
    "QUERY MSGS?":  12,  # do you have any stored messages?
    "QUERY CALL":   13,  # can you transmit a ping to callsign?
    # " ":          14,  # reserved
    "GRID":         15,  # this is my current grid locator
    "INFO?":        16,  # what is your info message?
    "INFO":         17,  # this is my info message
    "FB":           18,  # fine business
    "HW CPY?":      19,  # how do you copy?
    "SK":           20,  # end of contact
    "RR":           21,  # roger roger
    "QSL?":         22,  # do you copy?
    "QSL":          23,  # i copy
    "CMD":          24,  # command
    "SNR":          25,  # seen a station at the provided snr
    "NO":           26,  # negative confirm
    "YES":          27,  # confirm
    "73":           28,  # best regards, end of contact
    "ACK":          29,  # acknowledge
    "AGN?":         30,  # repeat message
    " ":            31,  # send freetext (weird artifact)
    "":             31,  # send freetext
}

snr_cmds = [25, 29]

nbasecall = 37 * 36 * 10 * 27 * 27 * 27

basecalls = {
    "<....>":     nbasecall + 1,   # incomplete callsign
    "@ALLCALL":   nbasecall + 2,   # ALLCALL group
    "@JS8NET":    nbasecall + 3,   # JS8NET group

    # continental dx
    "@DX/NA":     nbasecall + 4,   # North America DX group
    "@DX/SA":     nbasecall + 5,   # South America DX group
    "@DX/EU":     nbasecall + 6,   # Europe DX group
    "@DX/AS":     nbasecall + 7,   # Asia DX group
    "@DX/AF":     nbasecall + 8,   # Africa DX group
    "@DX/OC":     nbasecall + 9,   # Oceania DX group
    "@DX/AN":     nbasecall + 10,  # Antarctica DX group

    # itu regions
    "@REGION/1":  nbasecall + 11,  # ITU Region 1
    "@REGION/2":  nbasecall + 12,  # ITU Region 2
    "@REGION/3":  nbasecall + 13,  # ITU Region 3

    # generic
    "@GROUP/0":   nbasecall + 14,  # Generic group
    "@GROUP/1":   nbasecall + 15,  # Generic group
    "@GROUP/2":   nbasecall + 16,  # Generic group
    "@GROUP/3":   nbasecall + 17,  # Generic group
    "@GROUP/4":   nbasecall + 18,  # Generic group
    "@GROUP/5":   nbasecall + 19,  # Generic group
    "@GROUP/6":   nbasecall + 20,  # Generic group
    "@GROUP/7":   nbasecall + 21,  # Generic group
    "@GROUP/8":   nbasecall + 22,  # Generic group
    "@GROUP/9":   nbasecall + 23,  # Generic group

    # ops
    "@COMMAND":   nbasecall + 24,  # Command group
    "@CONTROL":   nbasecall + 25,  # Control group
    "@NET":       nbasecall + 26,  # Net group
    "@NTS":       nbasecall + 27,  # NTS group

    # reserved groups
    "@RESERVE/0": nbasecall + 28,  # Reserved
    "@RESERVE/1": nbasecall + 29,  # Reserved
    "@RESERVE/2": nbasecall + 30,  # Reserved
    "@RESERVE/3": nbasecall + 31,  # Reserved
    "@RESERVE/4": nbasecall + 32,  # Reserved

    # special groups
    "@APRSIS":    nbasecall + 33,  # APRS GROUP
    "@RAGCHEW":   nbasecall + 34,  # RAGCHEW GROUP
    "@JS8":       nbasecall + 35,  # JS8 GROUP
    "@EMCOMM":    nbasecall + 36,  # EMCOMM GROUP
    "@ARES":      nbasecall + 37,  # ARES GROUP
    "@MARS":      nbasecall + 38,  # MARS GROUP
    "@AMRRON":    nbasecall + 39,  # AMRRON GROUP
    "@RACES":     nbasecall + 40,  # RACES GROUP
    "@RAYNET":    nbasecall + 41,  # RAYNET GROUP
    "@RADAR":     nbasecall + 42,  # RADAR GROUP
    "@SKYWARN":   nbasecall + 43,  # SKYWARN GROUP
}

nbasegrid = 180 * 180
nusergrid = nbasegrid + 10
nmaxgrid = (1 << 15)-1

cqs = {
    0: "CQ CQ CQ",
    1: "CQ DX",
    2: "CQ QRP",
    3: "CQ CONTEST",
    4: "CQ FIELD",
    5: "CQ FD",
    6: "CQ CQ",
    7: "CQ",
}

hbs = {
    0: "HB",                  # HB
    1: "HB AUTO",             # HB AUTO
    2: "HB AUTO RELAY",       # HB AUTO RELAY
    3: "HB AUTO RELAY SPOT",  # HB AUTO RELAY SPOT
    7: "HB AUTO SPOT",        # HB AUTO       SPOT
    4: "HB RELAY",            # HB      RELAY
    5: "HB RELAY SPOT",       # HB      RELAY SPOT
    6: "HB SPOT",             # HB            SPOT
}
