from unittest import TestCase, skip
from js8py import Js8
from js8py.frames import Js8FrameDataCompressed, Js8FrameDirected, Js8FrameHeartbeat, Js8FrameCompound, Js8FrameCompoundDirected


class Js8Test(TestCase):
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
        test_data = [
            ("063545 -10 -0.2 1164 A  BYh0otuHOS3G         1", "SP5GSM: KO02")
        ]

        for raw_msg, expected in test_data:
            msg = Js8().parse_message(raw_msg)
            self.assertIsInstance(msg, Js8FrameCompound)
            self.assertEqual(str(msg), expected)

    @skip("implementation pending")
    def testFrameCompoundDirected(self):
        test_data = [
            ("063600 -10 -0.2 1163 A  JvLo5KJ5k+Le         2", "TODO")
        ]

        for raw_msg, expected in test_data:
            msg = Js8().parse_message(raw_msg)
            self.assertIsInstance(msg, Js8FrameCompoundDirected)
            self.assertEqual(str(msg), expected)
