from abc import ABC, abstractmethod
from .message import Js8Message
from .jsc import Jsc
from .huffman import HuffmanDecoder

import logging

logger = logging.getLogger(__name__)

alphanumeric = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ /@"  # callsign and grid alphabet


class Js8Frame(ABC):
    def __init__(self, msg: Js8Message):
        self.timestamp = msg.timestamp
        self.db = msg.db
        self.dt = msg.dt
        self.freq = msg.freq
        self.mode = msg.mode

    def bitsToInt(self, bits):
        ret = 0
        for bit in bits:
            ret = ret << 1 | bit
        return ret

    @abstractmethod
    def __str__(self):
        pass


class Js8FrameDataCompressed(Js8Frame):
    def __init__(self, msg: Js8Message):
        super().__init__(msg)
        self.message = Jsc().decompress(msg.bits[2:])

    def __str__(self):
        return self.message


class Js8FrameData(Js8Frame):
    def __init__(self, msg: Js8Message):
        super().__init__(msg)
        self.message = HuffmanDecoder().decode(msg.bits[2:])

    def __str__(self):
        return self.message


class Js8FrameDirected(Js8Frame):
    cmds = {
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

    def __init__(self, msg: Js8Message):
        super().__init__(msg)
        self.callsign_from = self.unpackCallsign(msg.bits[3:31], msg.bits[64])
        self.callsign_to = self.unpackCallsign(msg.bits[31:59], msg.bits[65])
        cmd = self.bitsToInt(msg.bits[59:64])
        self.cmd = [c for c, v in Js8FrameDirected.cmds.items() if v == cmd % 32][0]

        extra = self.bitsToInt(msg.bits[64:72])

        self.snr = None
        if extra:
            if cmd in Js8FrameDirected.snr_cmds:
                self.snr = extra - 31
            # else:
            #   unpacked.append(QString("%1").arg(extra-31));

    def unpackCallsign(self, bits, portable):
        value = 0
        for b in bits:
            value = value << 1 | b

        word = [""] * 6
        tmp = value % 27 + 10
        word[5] = alphanumeric[tmp]
        value = int(value / 27)

        tmp = value % 27 + 10
        word[4] = alphanumeric[tmp]
        value = int(value / 27)

        tmp = value % 27 + 10
        word[3] = alphanumeric[tmp]
        value = int(value / 27)

        tmp = value % 10
        word[2] = alphanumeric[tmp]
        value = int(value / 10)

        tmp = value % 36
        word[1] = alphanumeric[tmp]
        value = int(value / 36)

        tmp = value
        word[0] = alphanumeric[tmp]

        callsign = "".join(word)
        if callsign.startswith("3D0"):
            callsign = "3DA0" + callsign[3:]

        if callsign.startswith("Q") and 'A' <= callsign[1] and callsign[1] <= 'Z':
            callsign = "3X" + callsign[1:]

        callsign = callsign.strip()

        if portable:
            callsign = callsign + "/P"

        return callsign

    def __str__(self):
        result = "{0}: {1} {2}".format(self.callsign_from, self.callsign_to, self.cmd)
        if self.snr:
            result += " {0}".format(self.snr)
        return result
