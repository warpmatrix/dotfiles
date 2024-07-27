from dataclasses import dataclass

EventTopic = str


@dataclass
class Event:
    topic: EventTopic
    message: str
