"""
Simple in-process Event Bus.

Used in LOCAL_MODE instead of Kafka.
"""

from collections import defaultdict
from typing import Callable

_subscribers = defaultdict(list)


def subscribe(topic: str, handler: Callable):
    """
    Register a handler for a topic.
    """
    _subscribers[topic].append(handler)


def publish(topic: str, event: dict):
    """
    Publish an event to every subscriber.
    """

    for handler in _subscribers[topic]:
        handler(event)