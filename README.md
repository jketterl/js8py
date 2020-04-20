# js8py

A library to decode the output of the "js8" binary of [JS8Call](http://js8call.com/).

## Installation

`sudo python3 setup.py install`

## Usage

Example:

```python
from js8py import Js8

# raw message from the decoder
test_message = "140000 -11  0.4 1050 A  qBdgE+EP++++         2"

# extract information
decoded_message = Js8().parse_message(test_message)

# output string representation
print(str(decoded_message)) # "IN ITALY TODAY"
```