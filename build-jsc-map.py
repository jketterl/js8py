import re
import pickle


line_regex = re.compile("""\\s*{"([^"]+)".*, [0-9]+, [0-9]+},\\s*""")


def parseLine(line):
    matches = line_regex.match(line)
    if matches:
        return matches[1]


with open("/home/jakob/workspace/js8call/jsc_map.cpp", "r") as f:
    jsc_map = [parseLine(line) for line in f]

jsc_map = [line for line in jsc_map if line is not None]

with open("js8py/jsc_map.pickle", "wb") as f:
    pickle.dump(jsc_map, f)
