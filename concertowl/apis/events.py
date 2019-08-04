from concertowl.helpers import location


def filter_events(events, locations):
    return [e for e in events if e['city'] and e['country'] and location(e['city'], e['country']) in locations]


def unique_events(events):
    return list({
        event['title'].lower() + event['start_time'].split()[0] + event['city'].lower(): event
        for event in events
        if event.get('title') and event.get('start_time') and event.get('city')
    }.values())


def unique_collected_events(collected_events):
    return unique_events(e for events in collected_events for e in events)
