from typing import List

import pytest

from model.model_event import EventListener, ModelEvent
from service.subscribers import MappedSubscribers

class MockSubscriber(EventListener):
    listened: List[str]
    def __init__(self):
        self.listened = []

    def on_event(self, event: ModelEvent[str]):
        self.listened.append(event.get())

def test_subscribers():
    listener_map = [
        (MockSubscriber, str, "on_event")
    ]
    mapped_subs = MappedSubscribers(listener_map)

    sub1 = MockSubscriber()
    sub2 = MockSubscriber()

    mapped_subs.subscribe_all([sub1, sub2])

    events = ["event1", "event2", "event3"]

    for event in events:
        mapped_subs.publish(event)

    assert sub1.listened == events
    assert sub2.listened == events

def test_subscribers_ignore_prev_events():
    listener_map = [
        (MockSubscriber, str, "on_event")
    ]
    mapped_subs = MappedSubscribers(listener_map)
    events_before = ["event1", "event2", "event3"]
    for event in events_before:
        mapped_subs.publish(event)

    sub1 = MockSubscriber()
    mapped_subs.subscribe(sub1)

    events_after = ["event4", "event5", "event6"]
    for event in events_after:
        mapped_subs.publish(event)

    assert sub1.listened == events_after
    assert len(set(sub1.listened).intersection(set(events_before))) == 0


def test_subscribers_wrong_signature():
    listener_map = [
        (MockSubscriber, str, "not_existing_method")
    ]
    with pytest.raises(AttributeError):
        MappedSubscribers(listener_map)

def test_subscribers_no_event():
    listener_map = []
    mapped_subs = MappedSubscribers(listener_map)
    sub = MockSubscriber()
    with pytest.raises(ValueError):
        mapped_subs.subscribe(sub)











