from unittest.mock import patch

from django.test import TestCase
from django_q.tasks import result as result_q

from concertowl.apis import eventful
from concertowl.helpers import location


class EventfulTests(TestCase):

    def setUp(self):
        self.events = [{'title': str(i), 'start_time': str(i), 'venue': str(i), 'city': str(i)} for i in range(10)]
        self.testCountry = "test_country"
        self.testCity = "test_city"
        self.testTitle = "test_title"
        self.testArtist = "test_artist"
        self.testEvent = {
            'city': self.testCity,
            'country': self.testCountry,
            'title': self.testTitle,
            'start_time': '',
            'end_time': '',
            'venue': '',
            'artists': self.testArtist
        }

    def test_unique_collected_events(self):
        for name, events, expected in [
            ('empty', [], []),
            ('partially empty', [[self.events[0], self.events[1]], []], [self.events[0], self.events[1]]),
            ('filled', [[self.events[0]], [self.events[1]]], [self.events[0], self.events[1]]),
            ('duplicates', [[self.events[0], self.events[1]], [self.events[1]]], [self.events[0], self.events[1]])
        ]:
            with self.subTest(name):
                self.assertListEqual(eventful.unique_collected_events(events), expected)

    def test_add_events_for_artists(self):
        with patch.object(eventful, '_get_events', return_value=[self.testEvent]), patch.object(eventful, 'add_event') as add_mock:
            eventful.add_events_for_artists([self.testArtist], [location(self.testCity, self.testCountry)])
            add_mock.assert_called_with(self.testEvent)
