#!/usr/bin/python3
"""Provide subscribtion and publish news to subscribers"""

import queue
from typing import List

subs: List[queue.Queue] = []


def publish(news):
    """Pulish news to all subscripers"""
    for i in reversed(range(len(subs))):
        if subs[i].full():
            del subs[i]
            continue
        subs[i].put(news)


def subscribe():
    """Subscribe to get any future news"""
    q = queue.Queue(maxsize=5)
    subs.append(q)
    while True:
        msg = q.get(block=True, timeout=None)
        yield msg
