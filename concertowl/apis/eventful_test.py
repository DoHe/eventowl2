import unittest

from concertowl.apis.eventful import _unique_events


class EventfulTests(unittest.TestCase):

    def setUp(self):
        self.events = [{'title': i, 'start_time': i, 'venue': i} for i in range(10)]

    def test_unique_events(self):
        for name, events, expected in [
            ('empty', [], []),
            ('partially empty', [[self.events[0], self.events[1]], []], [self.events[0], self.events[1]]),
            ('filled', [[self.events[0]], [self.events[1]]], [self.events[0], self.events[1]]),
            ('duplicates', [[self.events[0], self.events[1]], [self.events[1]]], [self.events[0], self.events[1]])
        ]:
            with self.subTest(name):
                self.assertListEqual(_unique_events(events), expected)
