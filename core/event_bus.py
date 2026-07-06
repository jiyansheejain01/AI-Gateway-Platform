"""
Simple in-process Event Bus for LOCAL_MODE.

Acts as a lightweight replacement for Kafka during development.
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
    Publish an event to all subscribers.
    """

    for handler in _subscribers[topic]:
        handler(event)