from abc import ABC, abstractmethod
from .message import Js8Message
from .jsc import Jsc
from .huffman import HuffmanDecoder
from .constants import alphanumeric, directed_cmds, snr_cmds, basecalls, nbasegrid, cqs, hbs, nusergrid, nmaxgrid

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
        result = "{0}: {1}{2}".format(self.callsign_from, self.callsign_to, self.cmd)
        if self.snr is not None:
            result += " {0:0=+3}".format(self.snr)
        return result


class _Js8CompoundBase(Js8Frame):
    def __init__(self, msg: Js8Message):
        super().__init__(msg)
        packed_callsign = self.bitsToInt(msg.bits[3:53])
        self.callsign = self._unpackAlphanumeric50(packed_callsign)

    def _unpackAlphanumeric50(self, packed):
        word = [""] * 11

        tmp = packed % 38
        word[10] = alphanumeric[tmp]
        packed = int(packed / 38)

        tmp = packed % 38
        word[9] = alphanumeric[tmp]
        packed = int(packed / 38)

        tmp = packed % 38
        word[8] = alphanumeric[tmp]
        packed = int(packed / 38)

        tmp = packed % 2
        word[7] = "/" if tmp else " "
        packed = int(packed / 2)

        tmp = packed % 38
        word[6] = alphanumeric[tmp]
        packed = int(packed / 38)

        tmp = packed % 38
        word[5] = alphanumeric[tmp]
        packed = int(packed / 38)

        tmp = packed % 38
        word[4] = alphanumeric[tmp]
        packed = int(packed / 38)

        tmp = packed % 2
        word[3] = "/" if tmp else " "
        packed = int(packed / 2)

        tmp = packed % 38
        word[2] = alphanumeric[tmp]
        packed = int(packed / 38)

        tmp = packed % 38
        word[1] = alphanumeric[tmp]
        packed = int(packed / 38)

        tmp = packed % 39
        word[0] = alphanumeric[tmp]
        # packed = int(packed / 39)

        return "".join(word).replace(" ", "")

    def unpackGrid(self, value):
        if value > nbasegrid:
            return ""

        dlat = value % 180 - 90
        dlong = value / 180 * 2 - 180

        return self.deg2grid(dlong, dlat)[:4]

    def deg2grid(self, dlong, dlat):
        grid = bytearray(6)

        if dlong < -180:
            dlong += 360
        if dlong > 180:
            dlong -= 360

        nlong = int(60.0*(180.0-dlong)/5)

        n1 = int(nlong/240)
        n2 = int((nlong-240*n1)/24)
        n3 = int(nlong-240*n1-24*n2)

        grid[0] = ord('A') + n1
        grid[2] = ord('0') + n2
        grid[4] = ord('a') + n3

        nlat = int(60.0*(dlat+90)/2.5)

        n1 = int(nlat/240)
        n2 = int((nlat-240*n1)/24)
        n3 = int(nlat-240*n1-24*n2)

        grid[1] = ord('A') + n1
        grid[3] = ord('0') + n2
        grid[5] = ord('a') + n3

        return grid.decode("ascii")


class Js8FrameCompound(_Js8CompoundBase):
    def __init__(self, msg: Js8Message):
        super().__init__(msg)
        extra = self.bitsToInt(msg.bits[53:69])
        self.grid = None
        self.snr = None
        self.cmd = None
        if extra < nbasegrid:
            self.grid = self.unpackGrid(extra)
        elif nusergrid <= extra < nmaxgrid:
            cmd = extra - nusergrid
            if cmd & (1 << 7):
                #SNR
                self.cmd = "ACK" if cmd & (1 << 6) else "SNR"
                num = extra & ((1 << 6) - 1)
                self.snr = num - 31

    def __str__(self):
        res = "{0}:".format(self.callsign)
        if self.grid:
            res += " {0}".format(self.grid)
        elif self.cmd and self.snr:
            res += " {0} {1}".format(self.cmd, self.snr)
        return res


class Js8FrameHeartbeat(_Js8CompoundBase):
    def __init__(self, msg: Js8Message):
        super().__init__(msg)
        self.grid = self.unpackGrid(self.bitsToInt(msg.bits[54:69]))
        message_type = self.bitsToInt(msg.bits[69:72])
        messages = cqs if msg.bits[53] else hbs
        self.message = messages[message_type]

    def __str__(self):
        return "{0}: {1} {2}".format(self.callsign, self.message, self.grid)


class Js8FrameCompoundDirected(Js8FrameCompound):
    def __str__(self):
        res = "{0}".format(self.callsign)
        if self.grid:
            res += " {0}".format(self.grid)
        elif self.cmd and self.snr:
            res += " {0} {1}".format(self.cmd, self.snr)
        return res
