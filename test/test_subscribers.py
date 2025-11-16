from typing import List

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




