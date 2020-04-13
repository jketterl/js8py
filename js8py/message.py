from datetime import datetime, timezone

alphabet72 = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-+/?."


class Js8Message(object):
    def __init__(self, raw_message):
        # 122600 -13  0.3  697 A  yHYCHYCG++++         2
        # 01234567890123456789012345678901234567890123456789
        self.timestamp = self._parse_timestamp(raw_message[0:6])
        self.db = float(raw_message[7:10])
        self.dt = float(raw_message[11:15])
        self.freq = int(raw_message[16:20])
        self.mode = raw_message[21]
        self.payload = raw_message[24:45].strip()
        self.something = raw_message[45]
        self.bits = self._toBits()

    def _parse_timestamp(self, instring):
        ts = datetime.strptime(instring, "%H%M%S")
        return int(
            datetime.combine(datetime.utcnow().date(), ts.time()).replace(tzinfo=timezone.utc).timestamp() * 1000
        )

    def _toBits(self):
        indexes = [alphabet72.index(c) for c in self.payload]
        return [bit for index in indexes for bit in [int(index & (1 << (7 - i)) > 0) for i in range(2, 8)]]
