from datetime import datetime

import factory
from factory import fuzzy
from factory.django import DjangoModelFactory
import pytest
from pytest import fixture
import pytz

from concertowl import helpers
from concertowl.models import Artist, Event


class ArtistFactory(DjangoModelFactory):
    class Meta:
        model = Artist

    name = factory.Sequence(lambda n: 'artist{n}{n}{n}{n}{n}{n}{n}{n}'.format(n=n))


class EventFactory(DjangoModelFactory):
    class Meta:
        model = Event

    title = factory.Sequence(lambda n: 'title{n}{n}{n}{n}{n}{n}{n}{n}'.format(n=n))
    venue = factory.Sequence(lambda n: 'venue{n}{n}{n}{n}{n}{n}{n}{n}'.format(n=n))
    city = 'Berlin'
    country = 'Germany'
    start_time = fuzzy.FuzzyDateTime(datetime(2011, 1, 1, tzinfo=pytz.UTC))

    @factory.post_generation
    def artists(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for artist in extracted:
                self.artists.add(artist)


@fixture
def events():
    unq1 = EventFactory()
    unq2 = EventFactory()
    dup1 = EventFactory(
        title="duplicate 1",
        start_time=datetime(2019, 1, 1, 12, tzinfo=pytz.UTC),
        venue="dup venue",
        artists=[ArtistFactory(name="dup artist")],
    )
    dup3 = EventFactory(
        title="duplicate 3",
        start_time=datetime(2019, 1, 1, 12, tzinfo=pytz.UTC),
        venue="dup venue",
        artists=[ArtistFactory(name="dup artist")],
    )
    dup4 = EventFactory(
        title="duplicate 4",
        start_time=datetime(2019, 1, 1, 11, tzinfo=pytz.UTC),
        venue="dup venue",
        artists=[ArtistFactory(name="dup artist")],
    )
    dup5 = EventFactory(
        title="duplicate 5",
        start_time=datetime(2019, 1, 1, 11, tzinfo=pytz.UTC),
        venue="dup venue5",
        artists=[ArtistFactory(name="dup artist")],
    )
    dup6 = EventFactory(
        title="duplicate 6",
        start_time=datetime(2019, 1, 1, tzinfo=pytz.UTC),
        venue="dup venue5",
        artists=[ArtistFactory(name="dup artist1"), ArtistFactory(name="other artist")],
    )
    dup2 = EventFactory(
        title="duplicate 2",
        start_time=datetime(2019, 1, 1, 12, tzinfo=pytz.UTC),
        venue="dup venue",
        artists=[ArtistFactory(name="dup artist")],
    )

    return [
        unq1,
        unq2,
        dup1,
        dup2,
        dup3,
        dup4,
        dup5,
        dup6
    ]


@pytest.mark.django_db
def test_unique_events(events):
    actual = helpers.unique_events(events)
    assert len(actual) == 3
    titles = [e.title for e in actual]
    assert titles == ["title00000000", "title11111111", "duplicate 2"]
