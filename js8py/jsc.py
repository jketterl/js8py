import re

def readJscMap():
    line_regex = re.compile("""\\s*{"([^"]+)".*, [0-9]+, [0-9]+},\\s*""")

    def parseLine(line):
        matches = line_regex.match(line)
        if matches:
            return matches[1]

    with open("/home/jakob/workspace/js8call/jsc_map.cpp") as f:
        map = [parseLine(line) for line in f]

    return [line for line in map if line is not None]


class Jsc(object):
    size = 262144

    map = readJscMap()

    def decompress(self, bitvec):
        b = 4
        s = 7
        c = (2 ** b) - s

        out = []

        base = [0] * 8
        base[0] = 0
        base[1] = s
        base[2] = base[1] + s*c
        base[3] = base[2] + s*c*c
        base[4] = base[3] + s*c*c*c
        base[5] = base[4] + s*c*c*c*c
        base[6] = base[5] + s*c*c*c*c*c
        base[7] = base[6] + s*c*c*c*c*c*c

        bytes = []
        separators = []

        i = 0
        count = len(bitvec)
        while i < count:
            b = bitvec[i:i+4]
            if len(b) != 4:
                break
            byte = 0
            for bit in b:
                byte = (byte << 1) + bit
            bytes.append(byte)
            i += 4

            if byte < s:
                if count - i > 0 and bitvec[i]:
                    separators.append(len(bytes)-1)
                i += 1

        start = 0
        while start < len(bytes):
            k = 0
            j = 0

            while start + k < len(bytes) and bytes[start + k] >= s:
                j = j*c + (bytes[start + k] - s)
                k += 1
            if j >= Jsc.size:
                break

            if start + k >= len(bytes):
                break
            j = j*s + bytes[start + k] + base[k]

            if j >= Jsc.size:
                break

            out.append(Jsc.map[j])

            if separators and separators[0] == start + k:
                out.append(" ")
                separators.pop(0)

            start = start + (k + 1)

        # map is in latin1 format, not utf-8
        return "".join(out)
