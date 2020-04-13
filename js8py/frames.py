from abc import ABC, abstractmethod
from .message import Js8Message
from .jsc import Jsc
from .huffman import HuffmanDecoder
from .constants import alphanumeric, directed_cmds, snr_cmds, basecalls

import logging

logger = logging.getLogger(__name__)


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
    def __init__(self, msg: Js8Message):
        super().__init__(msg)
        self.callsign_from = self.unpackCallsign(msg.bits[3:31], msg.bits[64])
        self.callsign_to = self.unpackCallsign(msg.bits[31:59], msg.bits[65])
        cmd = self.bitsToInt(msg.bits[59:64])
        self.cmd = [c for c, v in directed_cmds.items() if v == cmd % 32][0]

        extra = self.bitsToInt(msg.bits[64:72])

        self.snr = None
        if extra:
            if cmd in snr_cmds:
                self.snr = extra - 31
            # else:
            #   unpacked.append(QString("%1").arg(extra-31));

    def unpackCallsign(self, bits, portable):
        value = self.bitsToInt(bits)

        for call, call_id in basecalls.items():
            if call_id == value:
                return call

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
            result += " {0:0=+3}".format(self.snr)
        return result
