import time
import unittest

from api.tools.timeFrameFinder import getTimeFrame


class TestGetTimeFrame(unittest.TestCase):
    def setUp(self):
        # Common setup for the tests
        self.current_time = int(time.time())
        self.sample_value = [
            {"epochtime": self.current_time + 4000, "value": 10},
            {"epochtime": self.current_time + 8000, "value": 30},
            {"epochtime": self.current_time + 12000, "value": 40},
            {"epochtime": self.current_time + 16000, "value": 20},
            {"epochtime": self.current_time + 20000, "value": 50},
        ]

    def test_basic_functionality(self):
        result = getTimeFrame(self.sample_value, split=1, dur=2, take_off=18)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["value"], 40)
        self.assertEqual(result[1]["value"], 50)

    def test_split_functionality(self):
        additional_value = [
            {"epochtime": self.current_time + 24000, "value": 60},
            {"epochtime": self.current_time + 28000, "value": 10},
        ]
        result = getTimeFrame(self.sample_value + additional_value, split=0, dur=3, take_off=18)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0]["value"], 20)
        self.assertEqual(result[1]["value"], 50)
        self.assertEqual(result[2]["value"], 60)

    def test_takeoff_time(self):
        future_value = [
            {"epochtime": self.current_time + 10000, "value": 100},
        ]
        result = getTimeFrame(future_value, split=1, dur=3, take_off=18)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["value"], 100)

    def test_no_future_value(self):
        past_value = [
            {"epochtime": self.current_time - 10000, "value": 5},
            {"epochtime": self.current_time - 5000, "value": 15},
        ]
        result = getTimeFrame(past_value, split=1, dur=3, take_off=18)
        self.assertEqual(len(result), 0)


if __name__ == '__main__':
    unittest.main()
