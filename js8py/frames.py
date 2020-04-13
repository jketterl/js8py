from .message import Js8Message
from .jsc import Jsc
from .huffman import HuffmanDecoder

import logging

logger = logging.getLogger(__name__)

alphanumeric = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ /@"  # callsign and grid alphabet


class Js8Frame (object):
    def __init__(self, msg: Js8Message):
        self.timestamp = msg.timestamp
        self.db = msg.db
        self.dt = msg.dt
        self.freq = msg.freq
        self.mode = msg.mode


class Js8FrameDataCompressed(Js8Frame):
    def __init__(self, msg: Js8Message):
        super().__init__(msg)
        self.message = Jsc().decompress(msg.bits[2:])


class Js8FrameData(Js8Frame):
    def __init__(self, msg: Js8Message):
        super().__init__(msg)
        self.message = HuffmanDecoder().decode(msg.bits[2:])


class Js8FrameDirected(Js8Frame):
    def __init__(self, msg: Js8Message):
        super().__init__(msg)
        self.callsign_from = self.unpackCallsign(msg.bits[3:31])
        self.callsign_to = self.unpackCallsign(msg.bits[31:59])

    def unpackCallsign(self, bits):
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

        #if(portable){
        #callsign = callsign.trimmed() + "/P";
        #}

        return callsign.strip()
