from .frames import Js8Frame, Js8FrameDataCompressed, Js8FrameData, Js8FrameDirected
from .message import Js8Message
from .constants import alphabet72

import logging

logger = logging.getLogger(__name__)

class Js8(object):
    def parse_message(self, msg) -> Js8Frame:
        parsed_msg = Js8Message(msg)

        bits = parsed_msg.bits
        if bits[0]:
            if bits[1]:
                return Js8FrameDataCompressed(parsed_msg)
            else:
                return Js8FrameData(parsed_msg)
        else:
            if bits[1]:
                if bits[2]:
                    return Js8FrameDirected(parsed_msg)
                else:
                    logger.debug("FrameCompoundDirected")
            else:
                if bits[2]:
                    logger.debug("FrameCompound")
                else:
                    logger.debug("FrameHeartbeat")
