from concertowl.helpers import location


def filter_events(events, locations):
    return [e for e in events if e['city'] and e['country'] and location(e['city'], e['country']) in locations]


def _unique_events(events):
    return list({
        event['title'] + event['start_time'] + event['venue']: event
        for event in events
    }.values())


def unique_collected_events(collected_events):
    return _unique_events(e for events in collected_events for e in events)
