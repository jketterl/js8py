from .frames import Js8Frame, Js8FrameDataCompressed, Js8FrameData, Js8FrameDirected
from .message import Js8Message

import logging

logger = logging.getLogger(__name__)

class Js8(object):
    def parse_message(self, msg) -> Js8Frame:
        parsed_msg = Js8Message(msg)

        bits = parsed_msg.bits
        if bits[0] and bits[1]:
            return Js8FrameDataCompressed(parsed_msg)
        elif bits[0] and not bits[1]:
            return Js8FrameData(parsed_msg)
        elif not bits[0] and not bits[1] and not bits[2]:
            logger.debug("FrameHeartbeat")
        elif not bits[0] and not bits[1] and bits[2]:
            logger.debug("FrameCompound")
        elif not bits[0] and bits[1] and not bits[2]:
            logger.debug("FrameCompoundDirected")
        elif not bits[0] and bits[1] and bits[2]:
            return Js8FrameDirected(parsed_msg)
