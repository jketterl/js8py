# taken from the js8call source
hufftable = {
    # char   code
    " ": "01",
    "E": "100",
    "T": "1101",
    "A": "0011",
    "O": "11111",
    "I": "11100",
    "N": "10111",
    "S": "10100",
    "H": "00011",
    "R": "00000",
    "D": "111011",
    "L": "110011",
    "C": "110001",
    "U": "101101",
    "M": "101011",
    "W": "001011",
    "F": "001001",
    "G": "000101",
    "Y": "000011",
    "P": "1111011",
    "B": "1111001",
    ".": "1110100",
    "V": "1100101",
    "K": "1100100",
    "-": "1100001",
    "+": "1100000",
    "?": "1011001",
    "!": "1011000",
    "\"": "1010101",
    "X": "1010100",
    "0": "0010101",
    "J": "0010100",
    "1": "0010001",
    "Q": "0010000",
    "2": "0001001",
    "Z": "0001000",
    "3": "0000101",
    "5": "0000100",
    "4": "11110101",
    "9": "11110100",
    "8": "11110001",
    "6": "11110000",
    "7": "11101011",
    "/": "11101010",
}


class HuffmanDecoder(object):
    def decode(self, payload):
        last_zero = len(payload) - payload[::-1].index(0) -1
        bits = payload[:last_zero]
        rem = [str(bit) for bit in bits]
        out = ""
        while len(rem) > 2:
            found = False
            for key, value in hufftable.items():
                if "".join(rem[:len(value)]) == value:
                    out += key
                    rem = rem[len(value):]
                    found = True
                    break
            if not found:
                break
        return out
