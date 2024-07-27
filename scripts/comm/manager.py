from comm.event import Event, EventTopic
from comm.listener.listener import Listener
from comm.utils import singleton


@singleton
class EventManager:
    def __init__(self) -> None:
        self.listeners: dict[EventTopic, list[Listener]] = {}

    def subscribe(self, topic: EventTopic, l: Listener):
        if self.listeners.get(topic) == None:
            self.listeners[topic] = []
        self.listeners[topic].append(l)

    def unsubscribe(self, topic: EventTopic, l: Listener):
        self.listeners[topic].remove(l)

    def notify(self, e: Event):
        topic = e.topic
        for l in self.listeners[topic]:
            l.notify(e)
