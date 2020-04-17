from unittest import TestCase, skip
from js8py import Js8
from js8py.frames import Js8FrameDataCompressed, Js8FrameDirected, Js8FrameHeartbeat, Js8FrameCompound, Js8FrameCompoundDirected, Js8FrameData


class Js8Test(TestCase):
    def testFrameData(self):
        test_data = [
            ("183500 -22  0.5 1519 A  iXvZfxW3Sju+         2", "KALHSPERA VNE"),
            ("201115 -16  0.6 1075 A  YNlWl7V+Uw-j         0", "F DIGI TOO DM7")
        ]

        for raw_msg, expected in test_data:
            msg = Js8().parse_message(raw_msg)
            self.assertIsInstance(msg, Js8FrameData)
            self.assertEqual(str(msg), expected)

    def testFrameDataCompressed(self):
        test_data = [
            ("140000 -11  0.4 1050 A  qBdgE+EP++++         2", "IN ITALY TODAY")
        ]

        for raw_msg, expected in test_data:
            msg = Js8().parse_message(raw_msg)
            self.assertIsInstance(msg, Js8FrameDataCompressed)
            self.assertEqual(str(msg), expected)

    def testFrameDirected(self):
        test_data = [
            ("151615 -11  0.3 2457 A  ViZoThL+C+aL         3", "G0CQZ: DF4MJ SNR -10"),
            ("161630 -19  0.3 1203 A  QrqjshWc6lq0         3", "DG3EK: DM5CQ ACK"),
            ("165430 -14  2.5 1697 A  Tuj1fVGGPoy0         1", "RV4CQ: @APRSIS GRID"),
            ("201915 -13  0.3  794 A  R43a8hMPfZqV         3", "EI2GYB: DF7FR ACK +00"),
            ("183445 -24  0.3 1520 A  VkrOrOOSTgK0         1", "M0SUY: SV1GGY>")
        ]

        for raw_msg, expected in test_data:
            msg = Js8().parse_message(raw_msg)
            self.assertIsInstance(msg, Js8FrameDirected)
            self.assertEqual(str(msg), expected)

    def testFrameHeartbeat(self):
        test_data = [
            ("172300 -12  0.4 1044 A  2jNlWSPIPQ-W         3", "LZ1CWK: CQ CQ CQ KN32"),
            ("192415 -15  0.4  953 A  1-ckNKyPOVwh         3", "G0CQZ: HB AUTO RELAY SPOT IO91"),
            ("200415 -13  0.5 1023 A  1mqQJL8Bv++u         3", "EA3ENR: CQ CQ CQ "),
        ]

        for raw_msg, expected in test_data:
            msg = Js8().parse_message(raw_msg)
            self.assertIsInstance(msg, Js8FrameHeartbeat)
            self.assertEqual(str(msg), expected)

    def testFrameCompound(self):
        # TODO: get verified samples
        test_data = [
            ("063545 -10 -0.2 1164 A  BYh0otuHOS3G         1", "SP5GSM:"),
            ("211315 -15  0.6 1250 A  B8giaUqYuUtG         1", "PE75OUW:"),
        ]

        for raw_msg, expected in test_data:
            msg = Js8().parse_message(raw_msg)
            self.assertIsInstance(msg, Js8FrameCompound)
            self.assertEqual(str(msg), expected)

    def testFrameCompoundDirected(self):
        # TODO: get verified samples
        test_data = [
            ("200345 -12  0.8 1001 A  H-jnbQvYe+ke         2", "G0WZM/A ACK -04"),
        ]

        for raw_msg, expected in test_data:
            msg = Js8().parse_message(raw_msg)
            self.assertIsInstance(msg, Js8FrameCompoundDirected)
            self.assertEqual(str(msg), expected)
